from matplotlib import pyplot as plt
from main import *

def plot_evoluiton(populate_func, fitness_func, fitness_limit, selection_func, crossover_func, mutation_func, generation_limit, title):
  best_per_generation = []

  # check the best one for each generation
  population = populate_func()
  for gen in range(generation_limit):
    population = sorted(population, key=lambda g: fitness_func(g), reverse=True)
    best_per_generation.append(fitness_func(population[0]))  # best genome in the generation

    if fitness_func(population[0]) >= fitness_limit:
      break

    next_generation = population[0:2]

    for _ in range(int(len(population)/2)-1):
      parents = selection_func(population, fitness_func)
      offspring_a, offspring_b = crossover_func(parents[0], parents[1])
      offspring_a = mutation_func(offspring_a)
      offspring_b = mutation_func(offspring_b)
      next_generation += [offspring_a, offspring_b]

    population = next_generation

  # draw the chart
  plt.figure(figsize=(10,6))
  plt.plot(range(1, len(best_per_generation)+1), best_per_generation, marker='o')
  plt.xlabel("Generation")
  plt.ylabel("Best fitness value")
  plt.title(title)
  plt.grid(True)
  plt.show()

  return population, best_per_generation

population, best_values = plot_evoluiton(
  populate_func=partial(generate_population, size=generate_population_size, genome_length=len(things)),
  fitness_func=partial(fitness, things=things, weight_limit=knapsack[0].weight),
  fitness_limit=fitness_limit,
  selection_func=roulette_wheel_selection_pair,
  crossover_func=single_point_crossover,
  mutation_func=mutation,
  generation_limit=generation_limit,
  title="Evolution chart"
)