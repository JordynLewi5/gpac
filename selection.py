
# selection.py

import random
import copy


# For all the functions here, it's strongly recommended to
# review the documentation for Python's random module:
# https://docs.python.org/3/library/random.html

# Parent selection functions---------------------------------------------------
def uniform_random_selection(population, n, **kwargs):
    # TODO: select n individuals uniform randomly
    selected = []
    for i in range(n):
        selected.append(random.choice(population))
    return selected


def k_tournament_with_replacement(population, n, k, **kwargs):
    # TODO: perform n k-tournaments with replacement to select n individuals
    selected = []
    for i in range(n):
        tournament = random.sample(population, k)
        winner = max(tournament, key=lambda x: x.fitness)
        selected.append(winner)
    return selected


#     return selection
def fitness_proportionate_selection(population, n, **kwargs):
    # Extract fitnesses
    fitnesses = [individual.fitness for individual in population]
    scaled = [fitness - min(fitnesses) + 1 for fitness in fitnesses]
    # Check for negative or equal fitness values
    min_fitness = min(fitnesses)
    
    # If there are negative fitnesses, scale all fitnesses so they are non-negative
    if min_fitness < 0:
        fitnesses = [f - min_fitness for f in fitnesses]
    elif all(f == fitnesses[0] for f in fitnesses):
        # If all fitnesses are equal, handle this case separately to avoid division by zero
        fitnesses = [1 for _ in fitnesses]
    
    # Perform selection
    selection = random.choices(population, weights=scaled, k=n)
    
    return selection


# Survival selection functions-------------------------------------------------
def truncation(population, n, **kwargs):
    # TODO: perform truncation selection to select n individuals
    sorted_individuals = list(sorted(population, key=lambda x: x.fitness))
    for i in sorted_individuals[-n:]:
        print(i.fitness)
    return sorted_individuals[-n:]


def k_tournament_without_replacement(population, n, k, **kwargs):
    # TODO: perform n k-tournaments without replacement to select n individuals
    # Note: an individual should never be cloned from surviving twice!
    selected = []
    copy_instance = copy.copy(population)
    for i in range(n):
        tournament = random.sample(copy_instance, k)
        winner = max(tournament, key=lambda x: x.fitness)
        selected.append(winner)
        copy_instance.remove(winner)
    return selected




# Yellow deliverable parent selection function---------------------------------
# SUS
def stochastic_universal_sampling(population, n, **kwargs):
    # TODO: select n individuals using stochastic universal sampling
    total_fit_val = sum([individual.fitness for individual in population])
    interval_distance = total_fit_val / n
    starting_point = random.uniform(0, interval_distance)
    selection_points = [starting_point + idx * interval_distance for idx in range(n)]
    sorted_population = sorted(population, key=lambda individual: individual.fitness)
    
    chosen_individuals = []
    accumulated_fit = 0
    idx = 0
    for select_point in selection_points:
        while accumulated_fit < select_point:
            accumulated_fit += sorted_population[idx].fitness
            idx += 1
        chosen_individuals.append(sorted_population[idx-1])
        
    return chosen_individuals

def scaled_fitness_proportionate_selection(population, n, **kwargs):
    # Extract fitnesses
    fitnesses = [individual.fitness for individual in population]
    scaled = [(fitness - min(fitnesses))**2 + 1 for fitness in fitnesses]
    # Check for negative or equal fitness values
    min_fitness = min(fitnesses)
    
    # If there are negative fitnesses, scale all fitnesses so they are non-negative
    if min_fitness < 0:
        fitnesses = [f - min_fitness for f in fitnesses]
    elif all(f == fitnesses[0] for f in fitnesses):
        # If all fitnesses are equal, handle this case separately to avoid division by zero
        fitnesses = [1 for _ in fitnesses]
    
    # Perform selection
    selection = random.choices(population, weights=scaled, k=n)
    
    return selection
