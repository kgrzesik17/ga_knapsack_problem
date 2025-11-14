from random import choices, random

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