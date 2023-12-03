
# gpac_population_evaluation.py

from fitness import *

# 2b TODO: Evaluate the population and assign base_fitness, fitness, and log
#          member variables as described in the Assignment 2b notebook.
def base_population_evaluation(population, parsimony_coefficient, experiment, **kwargs):
    if experiment.casefold() == 'green':
        # Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Sample call: score, log = play_GPac(controller, **kwargs)
        for individual in population:
            score, log = play_GPac(individual.genes, **kwargs)
            individual.size = individual.genes.count_nodes('root')
            individual.base_fitness = score
            individual.fitness = score - (parsimony_coefficient * individual.size)
            individual.log = log
    

    elif experiment.casefold() == 'yellow':
        # YELLOW: Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Use a different parsimony pressure technique than your green experiment.
        # Sample call: score, log = play_GPac(controller, **kwargs)
        for individual in population:
            score, log = play_GPac(individual.genes, **kwargs)
            individual.base_fitness = score
            individual.log = log
            individual.size = individual.genes.count_nodes('root')

        for (i, individual) in enumerate(population):
            other_individual = random.choice(population[:i] + population[i+1:])
            
            if individual.fitness == None:
                individual.fitness = individual.base_fitness
            if (other_individual.fitness == None):
                other_individual.fitness = other_individual.base_fitness

            # If the individual has a bigger tree than the other individual, penalize it
            if (individual.size > other_individual.size):
                individual.fitness -= (individual.size - other_individual.size) * parsimony_coefficient
        
    elif experiment.casefold() == 'red1':
        # RED1: Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Apply parsimony pressure as a second objective to be minimized, rather than a penalty.
        # Sample call: score, log = play_GPac(controller, **kwargs)
        pass

    elif experiment.casefold() == 'red2':
        # RED2: Evaluate a population of Pac-Man controllers against the default ghost agent.
        # Sample call: score, log = play_GPac(controller, **kwargs)
        pass

    elif experiment.casefold() == 'red3':
        # RED3: Evaluate a population where each game has multiple different Pac-Man controllers.
        # You must write your own play_GPac_multicontroller function, and use that.
        pass

    elif experiment.casefold() == 'red4':
        # RED4: Evaluate a population of ghost controllers against the default Pac-Man agent.
        # Sample call: score, log = play_GPac(None, controller, **kwargs)
        pass

    elif experiment.casefold() == 'red5':
        # RED5: Evaluate a population where each game has multiple different ghost controllers.
        # You must write your own play_GPac_multicontroller function, and use that.
        pass

#############################################################################################

# # gpac_population_evaluation.py

# from fitness import *

# # 2b TODO: Evaluate the population and assign base_fitness, fitness, and log
# #          member variables as described in the Assignment 2b notebook.
# def base_population_evaluation(population, parsimony_coefficient, experiment, **kwargs):
#     if experiment.casefold() == 'green':
#         # Evaluate a population of Pac-Man controllers against the default ghost agent.
#         # Sample call: score, log = play_GPac(controller, **kwargs)
#         pass

#     elif experiment.casefold() == 'yellow':
#         # YELLOW: Evaluate a population of Pac-Man controllers against the default ghost agent.
#         # Use a different parsimony pressure technique than your green experiment.
#         # Sample call: score, log = play_GPac(controller, **kwargs)
#         pass

#     elif experiment.casefold() == 'red1':
#         # RED1: Evaluate a population of Pac-Man controllers against the default ghost agent.
#         # Apply parsimony pressure as a second objective to be minimized, rather than a penalty.
#         # Sample call: score, log = play_GPac(controller, **kwargs)
#         pass

#     elif experiment.casefold() == 'red2':
#         # RED2: Evaluate a population of Pac-Man controllers against the default ghost agent.
#         # Sample call: score, log = play_GPac(controller, **kwargs)
#         pass

#     elif experiment.casefold() == 'red3':
#         # RED3: Evaluate a population where each game has multiple different Pac-Man controllers.
#         # You must write your own play_GPac_multicontroller function, and use that.
#         pass

#     elif experiment.casefold() == 'red4':
#         # RED4: Evaluate a population of ghost controllers against the default Pac-Man agent.
#         # Sample call: score, log = play_GPac(None, controller, **kwargs)
#         pass

#     elif experiment.casefold() == 'red5':
#         # RED5: Evaluate a population where each game has multiple different ghost controllers.
#         # You must write your own play_GPac_multicontroller function, and use that.
#         pass
