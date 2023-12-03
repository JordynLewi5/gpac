
# tree_genotype.py

import random
from copy import deepcopy
import numbers

class TreeGenotype():
    def __init__(self):
        self.genes = None
        self.fitness = 0
        self.base_fitness = 0
        self.log = None
        self.fights = 0
        self.sum_fitness = 0
        self.sum_base_fitness = 0
        self.size = 0

    @classmethod
    def initialization(cls, mu, **kwargs):
        # print(mu)
        population = [cls() for _ in range(mu)]

        # Uncomment these lines to see the primitives available:
        # print(kwargs['terminals'])
        # print(kwargs['nonterminals'])

        # 2a TODO: Initialize genes member variables of individuals
        #          in population using ramped half-and-half.
        #          Pass **kwargs to your functions to give them
        #          the sets of terminal and nonterminal primitives.

        depth_limit = kwargs['depth_limit']
        for i in range(mu):
            kwargs['depth_limit'] = random.randint(1, depth_limit)
            if (i % 2 == 0):
                population[i].genes = ParseTree().full(**kwargs)
            else:
                population[i].genes = ParseTree().grow(**kwargs)

        return population


    def to_string(self):
        # 2a TODO: Return a string representing self.genes in the required format.
        return self.genes.__str__()


    def recombine(self, mate, depth_limit, **kwargs):
        child = self.__class__()

        # 2b TODO: Recombine genes of mate and genes of self to
        #          populate child's genes member variable.
        #          We recommend using deepcopy, but also recommend
        #          that you deepcopy the minimal amount possible.
        
        # Deepcopy self and mate genes
        self_genes_copy = deepcopy(self.genes)
        mate_genes_copy = deepcopy(mate.genes)

        # Select random nodes from both trees
        self_random_node = self_genes_copy.select_random_node(self_genes_copy.root)
        mate_random_node = mate_genes_copy.select_random_node(mate_genes_copy.root)

        # Calculate the total number of nodes in the subtrees
        self_subtree_size = self_genes_copy.count_nodes(self_random_node)
        mate_subtree_size = mate_genes_copy.count_nodes(mate_random_node)

        # Check for depth limit
        if self_random_node.depth + mate_subtree_size <= depth_limit and mate_random_node.depth + self_subtree_size <= depth_limit:
            # Perform subtree crossover
            # Swap the subtrees at the selected nodes
            self_random_node.data, mate_random_node.data = mate_random_node.data, self_random_node.data
            self_random_node.left, mate_random_node.left = mate_random_node.left, self_random_node.left
            self_random_node.right, mate_random_node.right = mate_random_node.right, self_random_node.right

        # Assign the recombined tree to child
        child.genes = self_genes_copy

        return child


    def mutate(self, **kwargs):
        mutant = self.__class__()
        mutant.genes = deepcopy(self.genes)

        # 2b TODO: Mutate mutant.genes to produce a modified tree.
        # Perform grow on a random node in the tree excluding the root
        random_node = mutant.genes.select_random_node(mutant.genes.root)
        mutant.genes.grow(current_node=random_node, **kwargs)
        return mutant

class Node:
    def __init__(self, data, depth=0, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.depth = depth
        
        if self.data == 'C':
            self.data = round(random.uniform(-5, 5) * 100) / 100

    def is_leaf(self):
        return not self.left and not self.right

class ParseTree:
    def __init__(self):
        self.root = None

    def grow(self, current_depth=0, current_node=None, **kwargs):
        max_depth = kwargs['depth_limit']
        terminals = kwargs['terminals']
        nonterminals = kwargs['nonterminals']
        # If the tree is not empty, select a random node to grow from
        if self.root is not None:
            selected_node = self.select_random_node(self.root)
            # Grow the tree from the selected node
            self.grow_from_node(selected_node, current_depth, kwargs['depth_limit'], kwargs['terminals'], kwargs['nonterminals'])
        else:
            # If the tree is empty, start growing from the root
            self.root = self.create_node(current_depth, kwargs['depth_limit'], kwargs['terminals'], kwargs['nonterminals'])
            self.grow_from_node(self.root, current_depth, kwargs['depth_limit'], kwargs['terminals'], kwargs['nonterminals'])
        return self

    def grow_from_node(self, node, current_depth, max_depth, terminals, nonterminals):
        if node.is_leaf() and current_depth < max_depth:
            if node.data in terminals or isinstance(node.data, numbers.Number): return
            node.left = self.create_node(current_depth + 1, max_depth, terminals, nonterminals)
            self.grow_from_node(node.left, current_depth + 1, max_depth, terminals, nonterminals)
            node.right = self.create_node(current_depth + 1, max_depth, terminals, nonterminals)
            self.grow_from_node(node.right, current_depth + 1, max_depth, terminals, nonterminals)
        elif current_depth >= max_depth:
            node = self.create_node(current_depth, max_depth, terminals, ())
    
    def create_node(self, current_depth, max_depth, terminals, nonterminals):
        node = None
        if current_depth < max_depth:
            node = Node(random.choice(nonterminals + terminals), depth=current_depth)
        else:
            node = Node(random.choice(terminals), depth=current_depth)
        return node

    def full(self, current_depth=0, current_node=None, **kwargs):
        max_depth = kwargs['depth_limit']
        # Implement the full method here        
        if current_node is None:
            self.root = self.create_node(current_depth, max_depth, (), kwargs['nonterminals'])
            current_node = self.root
        
        if current_depth + 1 == max_depth:
            current_node.left = self.create_node(current_depth + 1, max_depth, kwargs['terminals'], ())
            current_node.right = self.create_node(current_depth + 1, max_depth, kwargs['terminals'], ())
        else:
            current_node.left = self.create_node(current_depth + 1, max_depth, (), kwargs['nonterminals'])
            current_node.right = self.create_node(current_depth + 1, max_depth, (), kwargs['nonterminals'])
            self.full(current_depth + 1, current_node.left, **kwargs)
            self.full( current_depth + 1, current_node.right, **kwargs)
        return self

    def evaluate(self, state, player, current_node=None):
        if current_node is None:
            current_node = self.root

        # If it's a leaf node, return its value based on the state
        if current_node.is_leaf():
            return self.evaluate_terminal(state, current_node, player)

        # Evaluate left child
        left_value = self.evaluate(state, player, current_node.left)

        # Evaluate right child
        right_value = self.evaluate(state, player, current_node.right)

        # Apply the operation at the current node to the values from the children
        return self.apply_operation(current_node.data, left_value, right_value)

    def evaluate_terminal(self, state, terminal, player):
        # Implement the logic to return the value for each terminal based on the state
        if player != 'm':
            player = int(player) + 1

        if terminal.data == 'G':
            if (player == 'm'):
                players = list(state['players'].values())
                player_pos = players[0]
                ghost_pos_array = [ghost for ghost in players[1:]]
                manhattan_distances = [manhattan(player_pos, ghost_pos) for ghost_pos in ghost_pos_array]
                return min(manhattan_distances)
            else:
                players = list(state['players'].values())
                ghost_pos = players[int(player)]
                other_ghost_pos_array = [ghost for ghost in players if ghost != ghost_pos]
                manhattan_distances = [manhattan(ghost_pos, other_ghost_pos) for other_ghost_pos in other_ghost_pos_array]
                return min(manhattan_distances)
        
        elif terminal.data == 'M':
            players = list(state['players'].values())
            player_pos = players[0]
            manhattan_distance_to_pacman = manhattan(player_pos, players[int(player)])
            return manhattan_distance_to_pacman
        
        elif terminal.data == 'P':
            # manahattan distance to nearest pill
            players = list(state['players'].values())
            if player == 'm':
                player_pos = players[0]
            else:
                player_pos = players[int(player)]
            pills = list(state['pills'])
            manhattan_distances = [manhattan(player_pos, pill) for pill in pills]
            return min(manhattan_distances)
        
        elif terminal.data == 'F':
            if state['fruit'] == None:
                return 0

            players = list(state['players'].values())
            if player == 'm':
                player_pos = players[0]
            else:
                player_pos = players[int(player)]
            fruit = state['fruit']
            return manhattan(player_pos, fruit)

        elif terminal.data == 'W':
            players = list(state['players'].values())
            if player == 'm':
                player_pos = players[0]
            else:
                player_pos = players[int(player)]
            walls = state['walls']
            
            wall_count = 0
            # Count borders
            for coordinate in player_pos:
                if coordinate == 0:
                    wall_count += 1
            # Count walls
            if (player_pos[0] > 0 and walls[player_pos[0] - 1][player_pos[1]]):
                wall_count += 1
            if (player_pos[0] < len(walls) - 1 and walls[player_pos[0] + 1][player_pos[1]]):
                wall_count += 1
            if (player_pos[1] > 0 and walls[player_pos[0]][player_pos[1] - 1]):
                wall_count += 1
            if (player_pos[1] < len(walls[0]) - 1 and walls[player_pos[0]][player_pos[1] + 1]):
                wall_count += 1
                
            return wall_count

        elif isinstance(terminal.data, numbers.Number):
            return terminal.data
        # Add other terminal cases if necessary

    def apply_operation(self, operation, left_value, right_value):
        # Implement the logic to apply the operation to the left and right values
        if operation == '+':
            return left_value + right_value
        elif operation == '-':
            return left_value - right_value
        elif operation == '*':
            return left_value * right_value
        elif operation == '/':
            # Gracefully handle division by zero
            return left_value / right_value if right_value != 0 else self.handle_division_by_zero(left_value)
        elif operation == 'RAND':
            return random.uniform(min(left_value, right_value), max(left_value, right_value))
        # Add other nonterminal cases if necessary

    def handle_division_by_zero(self, numerator):
        # Define a graceful way to handle division by zero
        return numerator  # or some other value you define

    def __str__(self, current_node=None, depth=0):
        # Implement the string representation of the tree here
        # Traverse tree with LNR traversal, print out the data
        if current_node is None:
            current_node = self.root

        result_str = '|' * depth + str(current_node.data) + '\n'

        if current_node.left:
            result_str += self.__str__(current_node.left, depth + 1)
        
        
        if current_node.right:
            result_str += self.__str__(current_node.right, depth + 1)

        return result_str

    def count_nodes(self, root):
        if root is None:
            return 0
        if root == 'root':
            root = self.root

        return 1 + self.count_nodes(root.left) + self.count_nodes(root.right)
    
    def select_random_node(self, root):
        count = self.count_nodes(root)
        rand_count = random.randint(1, count)
        stack = []
        current = root
        while stack or current:
            if current:
                stack.append(current)
                current = current.left  # Go to the leftmost node
            else:
                current = stack.pop()
                rand_count -= 1
                if rand_count == 0:
                    return current  # Found the nth node
                current = current.right  # Visit the right subtree

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
