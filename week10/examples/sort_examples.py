"""
Examples of two sorting algoritms
"""

import random

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
    

def test_sorts():
    """ Test the two sorting methods """
    
    random.seed(1)
    numbers = [random.randint(0, 100) for dummy in range(10)]
    
    print(numbers)
    print("Select sort:", selection_sort(numbers[:]))
    print("Merge sort", merge_sort(list(numbers[:])))
    
    
test_sorts()