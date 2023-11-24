
# tree_genotype.py

import random
from copy import deepcopy
from fitness import manhattan

class TreeGenotype():
    def __init__(self):
        self.fitness = None
        self.genes = None


    @classmethod
    def initialization(cls, mu, depth_limit, **kwargs):
        population = [cls() for _ in range(mu)]

        # Uncomment these lines to see the primitives available:
        # print(kwargs['terminals'])
        # print(kwargs['nonterminals'])

        # 2a TODO: Initialize genes member variables of individuals
        #          in population using ramped half-and-half.
        #          Pass **kwargs to your functions to give them
        #          the sets of terminal and nonterminal primitives.

        return population


    def to_string(self):
        # 2a TODO: Return a string representing self.genes in the required format.
        return 'Unimplemented'


    def recombine(self, mate, depth_limit, **kwargs):
        child = self.__class__()

        # 2b TODO: Recombine genes of mate and genes of self to
        #          populate child's genes member variable.
        #          We recommend using deepcopy, but also recommend
        #          that you deepcopy the minimal amount possible.

        return child


    def mutate(self, depth_limit, **kwargs):
        mutant = self.__class__()
        mutant.genes = deepcopy(self.genes)

        # 2b TODO: Mutate mutant.genes to produce a modified tree.

        return mutant
