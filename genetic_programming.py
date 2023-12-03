
# genetic_programming.py
import random
from base_evolution import BaseEvolutionPopulation

class GeneticProgrammingPopulation(BaseEvolutionPopulation):
    def generate_children(self):
        children = list()
        recombined_child_count = 0
        mutated_child_count = 0

        # 2b TODO: Generate self.num_children children by either:
        #          recombining two parents OR
        #          generating a mutated copy of a single parent.
        #          Use self.mutation_rate to decide how each child should be made.
        #          Use your Assignment Series 1 generate_children function as a reference.
        #          Count the number of recombined/mutated children in the provided variables.
        parents = self.parent_selection(self.population, self.num_children * 2, **self.parent_selection_kwargs)
        random.shuffle(parents)  # Shuffle to randomize pairings

        for i in range(0, len(parents), 2):
            if random.random() < self.mutation_rate:
                # Mutation: Use one parent
                mutated_child_count += 1
                child = parents[i].mutate(**self.mutation_kwargs)
            else:
                # Recombination: Use two parents
                recombined_child_count += 1
                child = parents[i].recombine(parents[i + 1], **self.recombination_kwargs)
            children.append(child)

            if len(children) >= self.num_children:
                break  # Stop when enough children are generated

        self.log.append(f'Number of children: {len(children)}')
        self.log.append(f'Number of recombinations: {recombined_child_count}')
        self.log.append(f'Number of mutations: {mutated_child_count}')

        return children