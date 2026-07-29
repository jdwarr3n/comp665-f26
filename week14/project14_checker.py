"""
Testing code for Project 14

Student will implement the following functions:

Volume(grid_values, grid_extents)
make_volume(z_coords, y_coords, x_coords, grid_fun)
read_volume(file_name)
"""

import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys;sys.modules['common_testing.common_testing'] = ct

#########################################################################
# Test case checkers for each machine-graded function in project

    
def check_Volume(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for Volume()
    """
    
    if type(computed).__name__ != type(expected).__name__:
        msg = "computed is not a Volume object"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    
    try:
        computed_extents = computed._extents
        expected_extents = expected._extents
        if not np.allclose(computed_extents, expected_extents):
            msg = "computed extents is " + str(computed_extents) + ", expected extents is " + str(expected_extents)
            ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
            return False
    except AttributeError:
        msg = "computed has no attribute extents"
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False      
    
    try:
        computed_data = computed._data
        expected_data = expected._data
        if type(computed_data) != type(expected_data):
            msg = "computed data is not a numpy array"
            ct.failed_large(fun_name, idx, fun_pts, 0.3, msg)
            return False
        if computed_data.shape != expected_data.shape:
            msg = "computed data shape is " + str(computed_data.shape) + ", expected data shape is " + str(expected_data.shape)
            ct.failed_large(fun_name, idx, fun_pts, 0.3, msg)
            return False
        if not np.allclose(computed._data, expected._data):
            msg = "computed data and expected data have different values"
            ct.failed_large(fun_name, idx, fun_pts, 0.5, msg)
            return False
    except:
        msg = "computed has no attribute data"
        ct.failed_large(fun_name, idx, fun_pts, 0.3, msg)
        return False
    
    return True
    

def check_make_volume(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for make_volume()
    """
    return check_Volume(computed, expected, inputs, idx, fun_name, fun_pts)


def check_read_volume(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for read_volume()
    """
    return check_Volume(computed, expected, inputs, idx, fun_name, fun_pts)


# Import test cases and test against student solutions using checker functions


CHECKER_DICT = {"Volume" : (check_Volume, 10),
                "make_volume" : (check_make_volume, 10),
                "read_volume" : (check_read_volume, 20)}                

ct.run_checkers("project14", CHECKER_DICT)





