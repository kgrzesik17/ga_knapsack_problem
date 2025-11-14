from main import *
import matplotlib.pyplot as plt
from functools import partial


# experiment parameters
crossover_methods = {
    "Single-point": single_point_crossover,
    "Two-point": two_point_crossover
}

mutation_rates = [0.1, 0.2, 0.3]

selection_methods = {
    "Roulette": roulette_wheel_selection_pair,
    "Ranking": ranking_selection_pair,
    "Tournament": tournament_selection_pair
}

# function to track the best fitness per generation
def run_evolution_with_history(
    populate_func,
    fitness_func,
    fitness_limit,
    selection_func=roulette_wheel_selection_pair,
    crossover_func=two_point_crossover,
    mutation_func=mutation,
    generation_limit=generation_limit
):
    population = populate_func()
    history = []

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )
        best_fitness = fitness_func(population[0])
        history.append(best_fitness)

        if best_fitness >= fitness_limit:
            break

        next_generation = population[0:2]

        for _ in range(int(len(population)/2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    return population, history



# different mutation and crossover types
def plot_mutation_crossover():
    plt.figure(figsize=(12, 8))

    for mutation_rate in mutation_rates:
        for name, crossover in crossover_methods.items():
            pop_func = partial(generate_population, size=generate_population_size, genome_length=len(things))
            fit_func = partial(fitness, things=things, weight_limit=knapsack[0].weight)
            _, history = run_evolution_with_history(
                populate_func=pop_func,
                fitness_func=fit_func,
                fitness_limit=fitness_limit,
                crossover_func=crossover,
                mutation_func=partial(mutation, probability=mutation_rate)
            )
            plt.plot(history, label=f"Mut={mutation_rate}, {name}")

    plt.title("Effect of mutation rate and crossover type")
    plt.xlabel("Generation")
    plt.ylabel("Best fitness")
    plt.legend()
    plt.grid(True)
    plt.show()


# comparison of ranking, roulette, and tornament selection
def plot_selection_all_methods(mutation_rate=0.2):
    plt.figure(figsize=(12, 8))

    for sel_name, sel_func in selection_methods.items():
        for cross_name, cross_func in crossover_methods.items():
            pop_func = partial(generate_population, size=generate_population_size, genome_length=len(things))
            fit_func = partial(fitness, things=things, weight_limit=knapsack[0].weight)
            _, history = run_evolution_with_history(
                populate_func=pop_func,
                fitness_func=fit_func,
                fitness_limit=fitness_limit,
                selection_func=sel_func,
                crossover_func=cross_func,
                mutation_func=partial(mutation, probability=mutation_rate)
            )
            plt.plot(history, label=f"{sel_name} + {cross_name}")

    plt.title(f"Comparison of all selection methods and crossover types (Mut={mutation_rate})")
    plt.xlabel("Generation")
    plt.ylabel("Best fitness")
    plt.legend()
    plt.grid(True)
    plt.show()


plot_mutation_crossover()
plot_selection_all_methods()