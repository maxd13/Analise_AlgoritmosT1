from linear_select import median_of_medians as linear_selection
from random import uniform

import time

def avg(ls):
    return sum(ls)/len(ls)

def bubble_sort(arr):
    n = len(arr) 
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def sort_selection(ls, k):
    assert type(k) is int
    assert type(ls) is list
    
    n = len(ls)
    if k <= 0 or k > n:
         raise Exception(f"""parameter k should be greater than 0 and less then the size of the input list.
                        Was = {k}.
                        Size of list was = {n}.
                        """
                        )
    return bubble_sort(ls)[k-1]


def main():
    n_instances = 10
    sizes = list(range(1000, 10001, 1000))
    data = dict()
    average_times = dict()

    for size in sizes:
        data[size] = []
        for k in range(n_instances):
            data[size].append( [uniform(0, 100000) for i in range(size)] )
    
    for size in sizes:
        sort_times = []
        linear_times = []
        for i in range(n_instances):
            k = size // 2
            # start time taking
            start = time.time()
            sort_selection(data[size][i], k)
            # stop counting time
            end = time.time()
            sort_times.append(end-start)

            # start taking time
            start = time.time()
            linear_selection(data[size][i], k)
            # stop taking time
            end = time.time()
            linear_times.append(end-start)

        average_times[size] = {
            'linear': avg(linear_times),
            'sort': avg(sort_times)
        }

    print(average_times)


if __name__ == '__main__':
    main()
