from collections import namedtuple
from functools import partial
from random import choices, randint, random, randrange, sample
import time
from typing import List

Thing = namedtuple('Thing', ['value', 'weight'])

# DATA
generate_population_size = 200
generation_limit = 100
mutation_probability = 0.2
verbose = True  # should print the output

file = open("large_scale/knapPI_1_100_1000_1", "r")  # file to analize
file_optimum = open("large_scale-optimum/knapPI_1_100_1000_1", "r")  # file with optimum

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
    knapsack.append(Thing(int(line[0]), int(line[1])))
    continue
  
  things.append(Thing(int(line[0]), int(line[1])))


# genetic representation of the solution
def generate_genome(length: int):
  return [1 if random() < 0.1 else 0 for _ in range(length)]


# generate new solutions
def generate_population(size: int, genome_length: int):
  return [generate_genome(genome_length) for _ in range(size)]


# fitness function to evaluate solutions
def fitness(genome, things, weight_limit: int):
  if(len(genome) != len(things)):
    raise ValueError("Genome and things must be of the same length")
  
  weight = 0
  value = 0

  for i, thing in enumerate(things):
    if genome[i] == 1:
      weight += thing.weight
      value += thing.value

      if weight > weight_limit:
        return 0
      
  return value


# selection - pair of solutions which will be the parents of two new solutions for the next generation
def roulette_wheel_selection_pair(population, fitness_func):
  # roulette wheel selection
  k = 2

  weights = [fitness_func(genome) for genome in population]

  # if all weight = 0, use uniform selection
  if sum(weights) == 0:
    return choices(population = population, k = 2)
  
  return choices(
    population=population,
    weights=weights,
    k=k
  )


def ranking_selection_pair(population, fitness_func):
  # ranking selection
  k = 2

  weights = [fitness_func(genome) for genome in population]

  # sort population by fitness
  sorted_population = [genome for _, genome in sorted(zip(weights, population), key=lambda x: x[0])]

  # assign ranks (1 for worst, n for best)
  n = len(sorted_population)
  ranks = list(range(1, n + 1))

  # use ranks as weighs for selection
  return choices(
    population=sorted_population,
    weights=ranks,
    k=k
  )


def tournament_selection_pair(population, fitness_func):
  # tournament selection
  k = 3

  weights = [fitness_func(genome) for genome in population]

  def select_one():
    tournament = sample(population, min(k, len(population)))
    return max(tournament, key=fitness_func)
  
  return [select_one(), select_one()]


# crossover - randomly cut genomes in half and combine
def single_point_crossover(a, b):
  # single point crossover
  if len(a) != len(b):
    raise ValueError("Genomes must be of the same length")
  
  length = len(a)
  if length < 2:
    return a, b
  
  p = randint(1, length - 1)

  offspring1 = a[0:p] + b[p:]
  offspring2 = b[0:p] + a[p:
                          ]
  return offspring1, offspring2  # first part of a, second part of b, and vice versa


def two_point_crossover(a, b):
  # two point crossover
  if len(a) != len(b):
    raise ValueError("Genomes must be of the same length")
  
  length = len(a)
  if length < 3:
    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]
  
  p1 = randint(1, length - 2)
  p2 = randint(p1 + 1, length - 1)

  offspring1 = a[0:p1] + b[p1:p2] + a[p2:]
  offspring2 = b[0:p1] + a[p1:p2] + b[p2:]

  return offspring1, offspring2


# mutation
def mutation(genome, num: int = 1, probability: float = mutation_probability):
    for _ in range(num):
        index = randrange(len(genome))
        if random() < probability:  # flip with probability
            genome[index] = 1 - genome[index]
    return genome



# evolution
def run_evolution(
    populate_func,
    fitness_func,
    fitness_limit: int,  # if fitness of the best solution exceeds the limit, it's done
    selection_func = roulette_wheel_selection_pair,
    # selection_func = ranking_selection_pair,
    # selection_func = tournament_selection_pair,
    # crossover_func = single_point_crossover,
    crossover_func = two_point_crossover,
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
    fitness, things=things, weight_limit=knapsack[0].weight
  ),
  fitness_limit=fitness_limit,
  generation_limit=generation_limit
)
end = time.perf_counter()

# print things based on genome
def genome_to_things(genome, thing):
  result_numer = 0
  result_tuple = []

  for i, thing in enumerate(things):
    if genome[i] == 1:
      result_tuple += [thing.value]
      result_numer += thing.value

  return [result_tuple, result_numer]

if verbose:
  print(f"Population size: {generate_population_size}")
  print(f"Mutation probability: {mutation_probability}")
  print(f"Number of generations: {generations + 1}")
  print(f"Time: {end - start}s")
  print(f"Best solution: {genome_to_things(population[0], things)[0]}")
  print(f"Item count: {len(genome_to_things(population[0], things)[0])}")
  print(f"Best solution value sum: {genome_to_things(population[0], things)[1]}")
  print(f"Optimum: {optimum}")