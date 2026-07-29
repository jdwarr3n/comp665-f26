"""
Testing code for Project 6

Student will implement the following functions:

random_arrangement(word_boxes, seed)
intersect_intervals(interval1, interval2)
intersect_boxes(box1, box2)
intersect_box_arrangement(test_box, word_arrangement)
montecarlo_arrangement(word_boxes, max_tries, seed)
spiral_arrangement(word_boxes, seed)
"""


import random
import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct    
# New: for importing the project code
import sys
sys.modules['common_testing.common_testing'] = ct

    
#########################################################################
# Test case checkers for each machine-graded function in project

def check_arrangement(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for one of the arrangement functions
    """
    if set(computed.keys()) != set(expected.keys()):
        msg = "computed and expected contains different words"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    
    for word in expected:
        
        computed_info = computed[word]
        expected_info = expected[word]
        
        if type(computed_info) !=  type(expected_info):
            msg = 'computed["' + word + '"] is type ' + str(type(computed_info)) + ", expected type is " + str(type(expected_info))
            ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
            return False
            
        if len(computed_info) !=  len(expected_info):
            msg = 'computed["' + word + '"] had length ' + str(len(computed_info)) + ", expected length is " + str(len(expected_info))
            ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
            return False

        computed_fontsize = computed_info[0]
        expected_fontsize = expected_info[0]      
        computed_layout = computed_info[1 :]
        expected_layout = expected_info[1 :]
        if not ((computed_fontsize == expected_fontsize) and (np.allclose(np.array(computed_layout), np.array(expected_layout)))):
            msg = 'computed["' + word + '"] is ' + str(computed_info) + ', expected["' + word + '"] is ' + str(expected_info)
            ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
            return False
        
        
    return True


def check_random_arrangement(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for random_arrangement()
    """
    return check_arrangement(computed, expected, inputs, idx, fun_name, fun_pts)


def check_intersect_intervals(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for intersect_intervals()
    """
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    return True
    
    
def check_intersect_boxes(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for intersect_boxes()
    """
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    return True
    

def check_intersect_box_arrangement(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for intersect_box_arrangement()
    """
    if computed != expected:
        msg = "computed and expected differ"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    return True

    

def check_montecarlo_arrangement(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for montecarlo_arrangement()
    """
    return check_arrangement(computed, expected, inputs, idx, fun_name, fun_pts)
    

def check_spiral_arrangement(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for spiral_arrangement()
    """
    return check_arrangement(computed, expected, inputs, idx, fun_name, fun_pts)
    


# Import test cases and test against student solutions using checker functions

CHECKER_DICT = { "random_arrangement" : (check_random_arrangement, 5),
                "intersect_intervals" : (check_intersect_intervals, 3),
                "intersect_boxes" : (check_intersect_boxes, 3),             
                "intersect_box_arrangement" : (check_intersect_box_arrangement, 3),
                "montecarlo_arrangement" : (check_montecarlo_arrangement, 8), 
                "spiral_arrangement" : (check_spiral_arrangement, 8)}                

ct.run_checkers("project6", CHECKER_DICT)






