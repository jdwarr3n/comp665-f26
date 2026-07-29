"""
Testing code for Project 12

Student will implement the following functions:

load_dem(dem_file)
compute_features(dem_array)
downsample_dem(dem_array)
"""

import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys;sys.modules['common_testing.common_testing'] = ct
    
    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_load_dem(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for load_dem()
    """    
    
    # look like type comparison in numpy is diecy - https://stackoverflow.com/questions/26921836/correct-way-to-test-for-numpy-dtype
    if type(computed) != np.ndarray:
        msg = "computed is not a numpy array"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if computed.dtype != np.uint16:
        msg = "computed dtype was " + str(computed.dtype) + ", expected type is np.uint16"
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False
    if computed.shape != expected.shape:
        msg = "computed has shape " + str(computed.shape) + ", expected has shape " + str(expected.shape)
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    if np.array_equal(computed // 10, expected):
        msg = "computed should be divided by a factor of 10"
        ct.failed_large(fun_name, idx, fun_pts, 0.6, msg)
        return False
    if not np.array_equal(computed, expected):
        msg = "computed and expected have different values"
        ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
        return False
    return True
    

def check_compute_features(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for compute_features()
    """
    if type(computed) != np.ndarray:
        msg = "computed is not a numpy array"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if computed.dtype != np.float64:
        msg = "computed dtype was " + str(computed.dtype) + ", expected type is np.float64"
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False
    if computed.shape != expected.shape:
        msg = "computed has shape " + str(computed.shape) + ", expected has shape " + str(expected.shape)
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    if not np.allclose(computed, expected):
        msg = "computed and expected have different values"
        ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
        return False
    return True


def check_downsample_dem(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for compute_features()
    """
    if type(computed) != np.ndarray:
        msg = "computed is not a numpy array"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if not np.issubdtype(computed.dtype, np.integer):
        msg = "computed dtype was " + str(computed.dtype) + ", expected type is np.integer"
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False
    if computed.shape != expected.shape:
        msg = "computed has shape " + str(computed.shape) + ", expected has shape " + str(expected.shape)
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    if not np.array_equal(computed, expected):
        msg = "computed and expected have different values"
        ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
        return False
    return True


# Import test cases and test against student solutions using checker functions

CHECKER_DICT = {"load_dem" : (check_load_dem, 10),
                "compute_features" : (check_compute_features, 10),
                "downsample_dem" : (check_downsample_dem, 10)}                

ct.run_checkers("project12", CHECKER_DICT)





