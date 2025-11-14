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