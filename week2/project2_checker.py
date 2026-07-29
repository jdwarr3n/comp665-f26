"""
Testing code for Project 2

Student will implement the following functions:

compute_distribution(flips, trials, seed)
"""

import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
sys.modules['common_testing.common_testing'] = ct

#########################################################################
# Test case checkers for each machine-graded function in project
TEST_CASES = ct.ProjectTests(["compute_distribution"], record_tests=False)
    
def check_compute_distribution(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for compute_distribution()
    """
    
    if len(computed) != len(expected):
        msg = "computed has length " + str(len(computed)) + ", expected has length " + str(len(expected))
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.1, msg)
        return False
    
    return True




#############################################################################
# Configure and run checkers

CHECKER_DICT = {"compute_distribution" : (check_compute_distribution, 10)}

ct.run_checkers("project2", CHECKER_DICT)


