#!/usr/bin/env python
from itertools import permutations#, repeat
from math import factorial as fat#, floor
#import numpy as np

def swap(i, j, list):
    l = list.copy()
    l[i], l[j] = l[j], l[i]
    return l 

# gives the neighborhood of each state of the game
# each state is an array of 9 positions containing numbers from 0 to 8.
# the array is treated as a matrix 3x3, such that every 3 elements of the array form a line.
# 0 marks the empty cell.
# We could have made a more general algorithm, for grids of arbitrary size.
# but this is unnecessary here.
def neighborhood (state):
    moves = []
    if state[0] is 0:
        moves.append(swap(0, 1, state))
        moves.append(swap(0, 3, state))
    elif state[1] is 0:
        moves.append(swap(1, 0, state))
        moves.append(swap(1, 2, state))
        moves.append(swap(1, 4, state))
    elif state[2] is 0:
        moves.append(swap(2, 1, state))
        moves.append(swap(2, 5, state))
    elif state[3] is 0:
        moves.append(swap(3, 0, state))
        moves.append(swap(3, 4, state))
        moves.append(swap(3, 6, state))
    elif state[4] is 0:
        moves.append(swap(4, 3, state))
        moves.append(swap(4, 1, state))
        moves.append(swap(4, 5, state))
        moves.append(swap(4, 7, state))
    elif state[5] is 0:
        moves.append(swap(5, 2, state))
        moves.append(swap(5, 4, state))
        moves.append(swap(5, 8, state))
    elif state[6] is 0:
        moves.append(swap(6, 3, state))
        moves.append(swap(6, 7, state))
    elif state[7] is 0:
        moves.append(swap(7, 6, state))
        moves.append(swap(7, 4, state))
        moves.append(swap(7, 8, state))
    elif state[8] is 0:
        moves.append(swap(8, 7, state))
        moves.append(swap(8, 5, state))
    else: raise Exception("not a valid state!")
    return moves

# hashes a state to a position in the hashtable/graph
# this is a perfect hash.
# the hashtable will be an array of permutations ordered lexicographically.
# the problem here is that the algorithm is quadratic in the size of the key
# and also depends on the complexity of the factorial funtion,
# although the key has a fixed sized of 9.
def hash(state):
    sum = 0
    for i in range(9):
        n = 0
        for j in range(i):
            if state[i] > state[j]: n += 1
        sum += (state[i] - n)*fat(8 - i)
    return sum

#creates the whole graph as a dictionary
# number of nodes: 9! = 362880
# 2 * number of edges = 2 * 4 * 8! + 3 * 4 * 8! + 4 * 1 * 8! = 4 * 8! * (2 + 3 + 1) = 24 * 8! 
# number of edges = 12 * 8! = 483840
# the graph is only about 7.34864...×10^-4 percent complete,
# therefore it is very sparse.
# switching the graph for a list, initialized as [None] * 362880, gives very similar time results.
# average running time is about 12 seconds.
# def make_graph():
#     graph = {}
#     for p in permutations(range(9)):
#         p = list(p)
#         # this line caused running times to jump to an average of 32 seconds.
#         #neighbors = [hash(x) for x in neighborhood(p)]
#         graph[hash(p)] = (p, neighborhood(p))
#     return graph

# here we are able to get running time averaging 3.6 seconds.
# but we have to prove that the permutation function generates the
# array in lexicographic order.
# this function used to be called fast_make_graph
def make_graph():
    graph = []
    for p in permutations(range(9)):
        p = list(p)
        graph.append((p, neighborhood(p)))
    return graph

# here are ways to test our claim.
# the tests pass.
# the first test runs on a "no news is good news" basis.
# def test1():
#     g = make_graph()
#     g2 = fast_make_graph()
#     for i in range(362880):
#         if g[i] != g2[i]:
#             print(f"diff at pos {i}: {g[i]} != {g2[i]}")
# def test2():
#     g = make_graph()
#     g2 = fast_make_graph()
#     bools = (g[i] == g2[i] for i in range(362880))
#     if all(bools):
#         print("PASSES!")
#     else:
#         print("FAILS!")
# because all tests pass we use the latter function rather than the former.
# by means of these tests we were able to make our original code about 9 times faster,
# from an average of 32 seconds, to an average of 3.6 seconds. These averages also have
# very low standard deviations (about a second between runs).

#creates the graph as a numpy.array
# this actually turned out to be slower so we will comment it out.
# def np_make_graph():
#     # array full of -1, with 13 colums.
#     # first 9 colums give the state,
#     # the last 4 give its neighbors.
#     graph = np.full((362880, 13), -1, dtype=np.int32)
#     for p in permutations(range(9)):
#         p = list(p)
#         neighbors = [hash(x) for x in neighborhood(p)]
#         aux = p + neighbors
#         if len(aux) < 13:
#             aux = aux + list(repeat(0, 13 - len(aux)))
#         graph[hash(p)] = np.array(aux)
#     return graph

# # cache by using depth first search
# def make_cache(initial_node, recursion_depth, cache):
#     ini = hash_state(initial_node)
#     if ini in cache:
#         return
#     cache[ini] = neighborhood(initial_node)
#     if recursion_depth is 0:
#         return
#     for n in cache[ini]:
#         if hash_state(n) in cache:
#             continue
#         make_cache(n, recursion_depth - 1, cache)

def main():
    pass

if __name__ == '__main__':
    main()

