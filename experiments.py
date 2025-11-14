from matplotlib import pyplot as plt
from main import *

mutation_rates = [0.1, 0.2, 0.3]
crossover_methods = {
  "Roulette": roulette_wheel_selection_pair,
  "Ranking": ranking_selection_pair,
  "Tournament": tournament_selection_pair
}

# results for mutation and crossover
results = {}
for mutation_prob in mutation_rates:
    for cross_name, cross_func in crossover_methods.items():
        population, best_per_gen = run_evolution(
            populate_func=partial(generate_population, size=generate_population_size, genome_length=len(things), things=things, weight_limit=weight_limit),
            fitness_func=partial(fitness, things=things, weight_limit=weight_limit),
            fitness_limit=fitness_limit,
            selection_func=roulette_wheel_selection_pair,
            crossover_func=cross_func,
            mutation_func=partial(mutation, probability=mutation_prob),
            generation_limit=generation_limit
        )
        label = f"{cross_name}, mutation={mutation_prob}"
        results[label] = best_per_gen

plt.figure(figsize=(10,6))
for label, best_values in results.items():
    plt.plot(range(1,len(best_values)+1), best_values, label=label)
plt.xlabel("Generacja")
plt.ylabel("Najlepsza wartość fitness")
plt.title("Mutacja vs krzyżowanie")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()