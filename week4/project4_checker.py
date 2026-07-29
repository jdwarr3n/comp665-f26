"""
Testing code for Project 4

Student will implement the following functions:

orbital_eqs(e, t)
solve_orbital_eqs(time_steps, speed)
extend_limits(limits, pad)
"""


import random
import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct    
    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_orbital_eqs(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for orbital_eqs()
    """
    
    if type(computed) != type(expected):
        msg = "type of computed = " + str(type(computed)) + ", type of expected = " + str(type(expected))
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False

    if not np.allclose(computed, expected):
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    return True
    
    
def check_solve_orbital_eqs(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for solve_orbital_eqs()
    """
    
    # Check type of computed
    if type(computed) != type(expected):
        msg = "computed is not a numpy array"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False        
    
    # Check shape of computed
    if computed.shape != expected.shape:
        msg = "computed has shape " + str(computed.shape) + ", expected has shape " + str(expected.shape)
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False       
    
    # Note that odeint produces slightly different answers on desktop vs Vocareum
    if not np.allclose(computed, expected, atol=3000):
        msg = "computed and expected positions differ by more than 3000 kilometers for speed = " + str(inputs[1])
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    
    return True
    

def check_extend_limits(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for extend_limits()
    """
    if not np.allclose(computed, expected):
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    return True



#############################################################################
# Configure and call checkers

CHECKER_DICT = {"orbital_eqs" : (check_orbital_eqs, 10),
                "solve_orbital_eqs" : (check_solve_orbital_eqs, 10),
                "extend_limits" : (check_extend_limits, 10)}                

ct.run_checkers("project4", CHECKER_DICT)



