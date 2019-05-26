#!/usr/bin/env python
from itertools import permutations
from math import factorial as fat

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

# creates the whole graph as a hashtable
# number of nodes: 9! = 362880
# 2 * number of edges = 2 * 4 * 8! + 3 * 4 * 8! + 4 * 1 * 8! = 4 * 8! * (2 + 3 + 1) = 24 * 8! 
# number of edges = 12 * 8! = 483840
# the graph is only about 7.34864...×10^-4 percent complete,
# therefore it is very sparse.
# here we are able to get running time averaging 3.6 seconds.
# but we have to prove that the permutation function generates the
# array in lexicographic order, so that our hash works.
# this is done in the test script

def make_graph():
    graph = []
    for p in permutations(range(9)):
        p = list(p)
        graph.append((p, neighborhood(p)))
    return graph

def BFS(G, s, visited):
    queue = [s]
    # distance from s, parent.
    visited[hash(s)] = (0, None)
    while queue:
        u = queue.pop(0)
        hu = hash(u)
        for v in G[hu][1]:
            hv = hash(v)
            if not visited[hv]:
                visited[hv] = (visited[hu][0] + 1, hu)
                queue.append(v)

def count_components(G):
    count = 0
    visited = [None] * 362880
    for i in range(362880):
        if not visited[i]:
            BFS(G, G[i][0], visited)
            count += 1
    return count

def hardest_problems(G):
    visited = [None] * 362880
    goal = list(range(1,9)) + [0]
    BFS(G, goal, visited)
    problems = []
    max = 0
    for i in range(362880):
        if not visited[i]: 
            continue
        elif visited[i][0] > max:
            max = visited[i][0]
            problems = [i]
        elif visited[i][0] == max:
            problems.append(i)

    solutions = []
    for p in problems:
        parent = visited[p][1]
        current_solution = [p]
        while parent:
            current_solution.append(parent)
            parent = visited[parent][1]
        solutions.append(current_solution)
    return (max, solutions)


def printState(state):
    print(state[0:3])
    print(state[3:6])
    print(state[6:9])


# Whole code takes an average of 42 seconds to run.
def main():
    g = make_graph()
    print(f"number of nodes: {len(g)}")
    print(f"number of edges: {sum([len(x[1]) for x in g])/2}")
    print(f"number of components: {count_components(g)}")
    d, solutions = hardest_problems(g)
    print(f"steps needed to solve hardest problems: {d}")
    print("hardest problems and solutions:\n")
    for s in solutions:
        print(f"problem: {g[s[0]][0]}")
        print("solution:")
        solution = [g[x][0] for x in s[1:]]
        for i in range(len(solution)):
            # print(f"    step {i+1}: {solution[i]}")
            print(f"    step {i+1}")
            printState(solution[i])

if __name__ == '__main__':
    main()

