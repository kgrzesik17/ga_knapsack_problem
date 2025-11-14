from functools import partial
from random import choices, randint, random, randrange
import time
from typing import List

# DATA
generate_population_size = 20
generation_limit = 100
mutation_probability = 0.5

file = open("low-dimensional/f1_l-d_kp_10_269", "r")  # file to analize
file_optimum = open("low-dimensional-optimum/f1_l-d_kp_10_269", "r")  # file with optimum

optimum = 0

for line in file_optimum:  # fetch optimum
  optimum = int(line)

fitness_limit = optimum

knapsack = []  # item_count | max_weight
things = []  # value | weight

for i, line in enumerate(file):
  line = line.strip()
  line = line.split()

  if i == 0:
    knapsack.append((int(line[0]), int(line[1])))
    continue
  
  things.append((int(line[0]), int(line[1])))


# genetic representation of the solution
def generate_genome(length: int):
  return [1 if random() < 0.1 else 0 for _ in range(length)]


# generate new solutions
def generate_population(size: int, genome_length: int):
  return [generate_genome(genome_length) for _ in range(size)]


# fitness function to evaluate solutions
def fitness(genome, things, weight_limit: int, item_limit: int):
  if(len(genome) != len(things)):
    raise ValueError("Genome and things must be of the same length")
  
  weight = 0
  value = 0
  item_count = 0

  for i, thing in enumerate(things):
    if genome[i] == 1:
      weight += thing.weight
      value += thing.value
      item_count += 1

      if weight > weight_limit or item_count > item_limit:
        return 0
      
  return value


# selection - pair of solutions which will be the parents of two new solutions for the next generation
def selection_pair(population, fitness_func):
  weights = [fitness_func(genome) for genome in population]

  # if all weight = 0, use uniform selection
  if sum(weights) == 0:
    return choices(population = population, k = 2)
  
  return choices(
    population=population,
    weights=weights,
    k=2
  )


# crossover - randomly cut genomes in half and combine
def single_point_crossover(a, b):
  if len(a) != len(b):
    raise ValueError("Genomes must be of the same length")
  
  length = len(a)
  if length < 2:
    return a, b
  
  p = randint(1, length - 1)
  return a[0:p] + b[p:], b[0:p] + a[p:]  # first part of a, second part of b, and vice versa


# mutation
def mutation(genome, num: int = 1, probability: float = mutation_probability):
  for _ in range(num):
    index = randrange(len(genome))
    genome[index] = genome[index] if random() < probability else abs(genome[index] - 1)
  return genome


# evolution
def run_evolution(
    populate_func,
    fitness_func,
    fitness_limit: int,  # if fitness of the best solution exceeds the limit, it's done
    selection_func = selection_pair,
    crossover_func = single_point_crossover,
    mutation_func = mutation,
    generation_limit = generation_limit
):
  # generate the first generation
  population = populate_func()

  # loop for generation limit times:
  for i in range(generation_limit):
    population = sorted(
      population, 
      key=lambda genome: fitness_func(genome),
      reverse=True
    )

    if fitness_func(population[0]) >= fitness_limit:
      break

    next_generation = population[0:2]

    # generate all the new solutions for the next generation
    for j in range(int(len(population) / 2) - 1):
      parents = selection_func(population, fitness_func)
      offspring_a, offspring_b = crossover_func(parents[0], parents[1])
      offspring_a = mutation_func(offspring_a)
      offspring_b = mutation_func(offspring_b)
      next_generation += [offspring_a, offspring_b]

    population = next_generation

  population = sorted(
    population,
    key=lambda genome: fitness_func(genome),
    reverse=True
  )

  return population, i

start = time.perf_counter()
population, generations = run_evolution(
  populate_func=partial(
    generate_population, size=generate_population_size, genome_length=len(things)
  ),
  fitness_func=partial(
    fitness, things=things, weight_limit=knapsack[0].weight, item_limit=knapsack[0].value
  ),
  fitness_limit=fitness_limit,
  generation_limit=generation_limit
)
end = time.perf_counter()

# print things based on genome
def genome_to_things(genome, things):
  result_numer = 0
  result_tuple = []

  for i, thing in enumerate(things):
    if genome[i] == 1:
      result_tuple += [thing.value]
      result_numer += thing.value

  return [result_tuple, result_numer]
