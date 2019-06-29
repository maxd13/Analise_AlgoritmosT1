
#!/usr/bin/env python 

from os import listdir, curdir
from os.path import isfile, join


class ProblemInstance():
    def __init__(self, n_items, backpack_size, v, w):
        self.n_items = n_items
        self.backpack_size = backpack_size
        self.v = v
        self.w = w
        # print('creating problem with variables: {}, {}, \n{}\n{}'.format(n_items, backpack_size, v, w))
    
    def solve(self):
        # start a matrix M [n_item][backpack_size]
        M = [ [0 for x in range(self.backpack_size + 1) ] for y in range(self.n_items + 1)]
        # print(M)
        for size in range(1, self.backpack_size+1):
            for n_item in range(1, self.n_items+1):
                # magic happens
                discounted_weight = size-self.w[n_item-1]
                discounted_weight = 0 if discounted_weight < 0 else discounted_weight
                M[n_item][size] = max(M[n_item-1][size], M[n_item][discounted_weight] + self.v[n_item-1])
        return M[-1][-1]


def read_problem(filename):
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
        print("Reading problem {}...".format(idx))
        problem = read_problem(f)
        print("Solving problem {}...".format(idx))
        result = problem.solve()
        print("result: {}".format(result))
        break


if __name__ == '__main__':
    main()