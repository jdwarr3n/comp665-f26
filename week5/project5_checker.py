"""
Testing code for Project 5

Student will implement the following functions:

invert_fun(complex_fun, complex_val)
julia_set(lmbd, z_0, num_returned, num_dropped)
iterate_mandel_fun(z_0)
mandel_table(real_values, imag_values)
newton_index(roots, z_0)
newton_table(roots, real_values, imag_values)
"""

import random
import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
sys.modules['common_testing.common_testing'] = ct

# Build better tests, use failed_small and fail_large
    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_invert_fun(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for invert_fun()
    """
    if len(computed) != len(expected):
        msg = "computed has length " + str(len(computed)) + ", expected has length " + str(len(expected))
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    if not np.allclose(np.sort(computed), np.sort(expected)):       # This test is a little dodgy
        msg = "computed = " + str(computed) + ", expected =" + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
        return False
    return True
    
    
    
def check_julia_set(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for julia_set()
    """
    if not isinstance(computed, list):
        msg = "computed is not a list"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False        
    if len(computed) != len(expected):
        msg = "computed has length " + str(len(computed)) + ", expected has length " + str(len(expected))
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if not np.allclose(computed, expected):
        msg = "computed and expected differ"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    return True


def check_iterate_mandel(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for iterate_mandel()
    """
    if not np.issubdtype(type(computed), np.signedinteger):
        msg = "computed is not an integer"
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False 
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
        return False
    return True


def check_mandel_table(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for mandel_table()
    """
    if type(computed) != np.ndarray:
        msg = "computed is not a numpy array"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if computed.shape != expected.shape:
        msg = "computed has shape " + str(computed.shape) + ", expected has shape " + str(expected.shape)
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if not np.allclose(computed, expected):
        msg = "computed and expected differ"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    return True
    
    
def check_newton_index(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for newton_index()
    """
    if not np.issubdtype(type(computed), np.signedinteger):
        msg = "computed is not an integer"
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False 
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
        return False
    return True


def check_newton_table(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for newton_table()
    """
    if type(computed) != np.ndarray:
        msg = "computed is not a numpy array"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if computed.shape != expected.shape:
        msg = "computed has shape " + str(computed.shape) + ", expected has shape " + str(expected.shape)
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if not np.allclose(computed, expected):
        msg = "computed and expected differ"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    return True

    


#############################################################################
# Configure and call checkers

CHECKER_DICT = {"invert_fun" : (check_invert_fun, 5),
                "julia_set" : (check_julia_set, 5),
                "iterate_mandel" : (check_iterate_mandel, 5),
                "mandel_table" : (check_mandel_table, 5),
                "newton_index" : (check_newton_index, 5),
                "newton_table" : (check_newton_table, 5)}                

ct.run_checkers("project5", CHECKER_DICT)





