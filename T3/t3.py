#!/usr/bin/env python 
import os

# B - tamanho da mochila
# n - número de  itens diferentes
# wi - tamanho do item i
# vi - valor do item i


def parse(content):
    first_line = content[0].split()
    n = int(first_line[0])
    B = int(first_line[1])
    # lista de valores
    v = []
    # lista de tamanhos
    w = []
    for i in range(1, n+1):
        line = content[i].split()
        v.append(int(line[0]))
        w.append(int(line[1]))
    return n, B, v, w


def knapsack(n, B, v, w):
    pass


def main():
    for i in range(1, 9):
        filename = 'inst' + str(i)
        instance_file = os.path.join('instancias', filename)
        f = open(instance_file, 'r')
        content = f.read().splitlines()
        f.close()
        n, B, v, w = parse(content)
        value, items = knapsack(n, B, v, w)



if __name__ == '__main__':
    main()