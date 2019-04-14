#!/usr/bin/env python 
from math import ceil


# O(n log n)
def simple_median(ls):
    n = len(ls)
    sort_list = sorted(ls)
    return sort_list[n // 2]
    

def median_of_medians(ls, k):
    n = len(ls) # O(1)
    if k <= 0 or k > n:
         raise Exception(f"""parameter k should be greater than 0 and less then the size of the input list.
                        Was = {k}.
                        Size of list was = {n}.
                        """
                        )
    if n <= 5:
        return sorted(ls)[k - 1]
    
    group_medians = [simple_median(ls[i : i + 5]) for i in range(0, n, 5)] # O(n),
        # python list slicing is O(i + 5 - i = 5) for a range of 5.
        # simple_median for a list of size 5 can be assumed O(1).
        # if the list is not a multiple of 5, the last n % 5 elements will be treated just like the others.
    n = ceil(len(group_medians) / 2)
        # for odd lengths this gets the middle point.
    group_mom = median_of_medians(group_medians, n)
    
    #left = [x for x in ls if x < group_mom] # O(n)
    #right = [x for x in ls if x > group_mom] # O(n)
    # unfortunately this is not optimized, even though it is readable.

    left = []
    right = []
    for x in ls:
        if x < group_mom: left.append(x)
        elif x > group_mom: right.append(x)
          

    left_len = len(left)
    right_len = len(right)
    middle_len = len(ls) - right_len - left_len
    
    if left_len <= (k - 1) < (left_len + middle_len) : return group_mom
    if k - 1 < left_len   : return median_of_medians(left, k)
    if k-1 >= (left_len + middle_len)  : return median_of_medians(right, k - left_len - middle_len)

def main():
     # ls = range(1, 101) # median 50
    
    # test case for repeated numbers
    test_cases = [(9, 9), (10, 10), (11, 11), (12, 11), (13, 11), (14, 11), (15, 15)]
    ls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11, 15, 16, 17, 18, 19, 20, 21]
    for case in test_cases:
        result = median_of_medians(ls, case[0])
        print("Testing case answer: {}, MoM: {}...".format(case[0], median_of_medians(ls, case[1])), end=' ')
        assert case[1] == result
        print('Ok.')


if __name__ == '__main__':
    main()