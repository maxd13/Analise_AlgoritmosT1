
#!/usr/bin/env python 

from os import listdir, curdir
from os.path import isfile, join
from random import randint

import copy



class ProblemInstance():
    """ 
    class to represent each problem instance
    """
    def __init__(self, n_items, backpack_size, v, w):
        self.n_items = n_items
        self.backpack_size = backpack_size
        self.v = v
        self.w = w
        # print('creating problem with variables: {}, {}, \n{}\n{}'.format(n_items, backpack_size, v, w))
    
    @staticmethod
    def get_max(sequence):
        """
        Function that return the max value and
        its index in a sequence
        
        :param sequence: iterable of integers in which to find max
        :type sequence: iterable
        :return: a tuple containing the index and value of max element
        :rtype: tuple
        """
        maximum = sequence[0]
        max_idx = 0
        for idx, e in enumerate(sequence):
            if e > maximum:
                maximum = e
                max_idx = idx
        return (max_idx, maximum)


    def solve(self):
        """
        Solves the knapsack problem using DP (Dinamic Programming)
        in an iterative form.
        To fill each element of the DP matrix, it uses one element
        to the left and up to 10 elements up, which means it finds
        the solution in O(n^2).
        
        :return: (best solution value, quantity of each item)
        :rtype: tuple
        """
        # start a matrix M [n_item][backpack_size] to hold solution values
        M = [ [0 for x in range(self.backpack_size + 1) ] for y in range(self.n_items + 1)]
        # start matrix L to hold the items quantities of each solution 
        L = [ [[] for x in range(self.backpack_size + 1) ] for y in range(self.n_items + 1)]

        for size in range(1, self.backpack_size+1):
            for n_item in range(1, self.n_items+1):
                # here the magic happens
                # with_item will hold all values possible with 
                # 1..n (n<=10) itens of type item_n in the backpack
                # each time we access w or v we use [n_item-1] because n_item
                # is zero indexed, meaning M[n_item = 0] represent no itens,
                # and M[n_item = 1] represent solutions including only the first item. 
                with_item = []
                for i in range(1, 10):
                    discounted_weight = size - i * self.w[n_item-1]
                    if discounted_weight < 0:
                        # does not fit in the backpack
                        continue
                    with_item.append(M[n_item-1][discounted_weight] + i*self.v[n_item-1])
                max_idx, max_value = self.get_max([M[n_item-1][size], *with_item])
                
                # if max_idx:
                L[n_item][size] = copy.deepcopy(L[n_item-1][size - max_idx * self.w[n_item-1]])
                L[n_item][size].append(max_idx)
                # else:
                    
                
                # L[size].append(max_idx)
                M[n_item][size] = max_value

        return M[-1][-1], L[-1][-1]


def read_problem(filename):
    """ 
    Reads problem info from file and returns and instance of
    ProblemInstance class representing the problem
    
    :param filename: name of the file to be opened
    :type filename: string
    :return: ProblemInstance representing the problem
    :rtype: ProblemIntance
    """
    with open(join(curdir, 'problem_instances', filename)) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        # first row gives us n_items and backpack_size
        content0 = content.pop(0).split(' ')
        n_items = int(content0[0])
        backpack_size = int(content0[1])
        # next lines gives us item value and weight
        v = []
        w = []
        for l in content:
            value, weight = l.split(' ')
            v.append(int(value))
            w.append(int(weight))
        return ProblemInstance(n_items, backpack_size, v, w)


def main():
    # get all problem instances
    print("Checking file instances...")
    instance_files = [f for f in listdir(join(curdir, 'problem_instances'))]
    instance_files = list(filter(lambda f: str.startswith(f,'inst'), instance_files))
    instance_files.sort()
    if len(instance_files) == 0:
        print("Error: no instance files found.")
    print("{} instance files found.".format(len(instance_files)))
    for idx, f in enumerate(instance_files):
        problem = read_problem(f)
        result, solution = problem.solve()

        print("\nMelhor valor obtido na instancia {}: {}".format(idx+1, result))
        color_number = randint(91, 96)
        for i, item in enumerate(solution):
            color = ''
            if item:
                color = '\033[{}m'.format(str(color_number))
            print("\t{}Foram usados {} do item numero {}{}".format(color, item, i+1, '\033[0m'))


if __name__ == '__main__':
    main()