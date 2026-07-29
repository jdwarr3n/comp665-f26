"""
Testing code for Project 3

Student will implement the following functions:

read_series(file_name)
clean_series(file_name)
isodate_to_day(isodate)
"""

import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct

#########################################################################
# Test case checkers for each machine-graded function in project
    
    
def check_read_series(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for read_series()
    """
    if len(computed) != len(expected):
        msg = "computed has length " + str(len(computed)) + " and expected has length " + str(len(expected))
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if computed != expected:
        msg = "computed prices and expected prices differ"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False   
    return True


    
def check_clean_series(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for clean_series()
    """
    if len(computed) != len(expected):
        msg = "computed has length " + str(len(computed)) + " and expected has length " + str(len(expected))
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    
    for row in computed:
        if not isinstance(row[1], float):
            msg = "computed price is not a float"
            ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
            return False
        
    computed_prices = np.array([row[1] for row in computed])
    expected_prices = np.array([row[1] for row in expected])
    if not np.allclose(computed_prices, expected_prices):
        msg = "computed prices and expected prices differ"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    
    computed_days = [row[0] for row in computed]
    expected_days = [row[0] for row in expected]
    if computed_days != expected_days:
        msg = "computed days and expected days differ"
        ct.failed_large(fun_name, idx, fun_pts, 0.5, msg)
        return False
        
    return True


TOLERANCE = 10e-06
    
def check_isodate_to_day(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for isodate_to_day()
    """
    if abs(computed - expected) > TOLERANCE:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.3, msg)
        return False
    return True


#############################################################################
# Configure and call checkers

CHECKER_DICT = {"read_series" : (check_read_series, 10),
                "clean_series" : (check_clean_series, 10),
                "isodate_to_day" : (check_isodate_to_day, 10)}

ct.run_checkers("project3", CHECKER_DICT)



