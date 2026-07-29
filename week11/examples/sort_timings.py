"""
Plots comparing the efficiency of two sorting algoritms
"""

import random
import time
import numpy as np
import matplotlib.pyplot as plt

def selection_sort(numbers):
    """
    Input: numpy array of numbers
    
    Output: List of numbers sorted in ascending order
    
    Note: mutates input list
    """
    
    for idx in range(len(numbers)):
        min_idx = numbers.index(min(numbers[idx:]))
        numbers[idx], numbers[min_idx] = numbers[min_idx], numbers[idx]
    return numbers

def merge_sort(numbers):
    """
    Input: numpy array of numbers
    
    Output: List of numbers sorted in ascending order
    """
    if len(numbers) == 1:
        return numbers
    else:
        mid = len(numbers) // 2
        return merge(merge_sort(numbers[: mid]), merge_sort(numbers[mid :]))
    
    
def merge(num1, num2):
    """
    Input: Two list num1 and num2 of numbers in sorted order
    
    Output: Merge list of numbers in sorted order
    """
    answer = []
    idx1, idx2 = 0, 0
    
    while idx1 < len(num1) and idx2 < len(num2):
        if num1[idx1] <= num2[idx2]:
            answer.append(num1[idx1])
            idx1 += 1
        else:
            answer.append(num2[idx2])
            idx2 += 1
            
    return answer + num1[idx1:] + num2[idx2:]



def plot_sort_timings(sort1, sort2, sort1_name, sort2_name):
    """
    Input: functions sort1, sort2 that sort a list of number
    optional string title
    
    Action: Plots the running times for both sorting method on
    lists of increasing sizes
    """
    
    random.seed(1)
    
    sort1_timings = []
    sort2_timings = []
    for size in range(1000, 10000, 100):
        numbers = [random.randint(0, 100) for dummy in range(size)]
        
        begin_time = time.time()
        sort1(numbers[:])
        end_time = time.time()
        sort1_timings.append((size, end_time - begin_time))
        
        begin_time = time.time()
        sort2(numbers[:])
        end_time = time.time()
        sort2_timings.append((size, end_time - begin_time))
        
    sort1_array = np.array(sort1_timings)
    sort2_array = np.array(sort2_timings)
    
    plt.plot(sort1_array[1:, 0], sort1_array[1:, 1], label=sort1_name)
    plt.plot(sort2_array[1:, 0], sort2_array[1:, 1], label=sort2_name)
    plt.title("Efficiency of " + sort1_name + " vs. " + sort2_name)
    plt.xlabel("Size of input list")
    plt.ylabel("Time in seconds")
    plt.legend()
    plt.show()    
    
plot_sort_timings(selection_sort, merge_sort, "Selection sort", "Merge sort")



