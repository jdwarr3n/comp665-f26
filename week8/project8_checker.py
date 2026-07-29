"""
Testing code for Project 8

Student will implement the following functions:

get_county_attributes(svg_file_name)
get_boundary_vertices(county_boundary)
make_county_dataframe(svg_file_name)
"""

import random
import numpy as np
import pandas as pd
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys
sys.modules['common_testing.common_testing'] = ct


#####################################################################
# Helper function for comparing two pandas dataframes

def compare_df(df1, df2):
    """
    Input: Dataframes df1, df2 sharing same order sequence of columns
    
    Output: Tuple consisting of boolean, float, string
    Boolean indicates whether two dataframes are equal,
    float is percentagage credit, string is error message
    """
    
    cp1 = df1.copy()
    cp2 = df2.copy()
    
    # Check if dataframes have same number of columns
    if len(cp1.columns) != len(cp2.columns):
        msg = "Computed has " + str(len(cp1.columns)) + " columns, expected has " + str(len(cp2.columns)) + " columns"
        return (False, 0, msg)
    
    # Check if dataframes have same number of rows
    if cp1.shape[0] != cp2.shape[0]:
        msg = "Computed has " + str(cp1.shape[0]) + " rows, expected has " + str(cp2.shape[0]) + " rows"
        return (False, 0.2, msg)
    
    # Check if dataframes have set of indices
    if set(cp1.index) != set(cp2.index):
        msg = "Computed and expected have differing row indices"
        return (False, 0.3, msg)
    
    # Check if corresponding rows have equal values within tolerance
    for idx in cp1.index:
        if not np.allclose(cp1.loc[idx], cp2.loc[idx]):
            msg = "compute.loc[" + str(idx) + "]  = " + str(list(cp1.loc[idx])) + \
                  ", expected.loc[" + str(idx) + "] = " + str(list(cp2.loc[idx]))
            return (False, 0.4, msg)
    return (True, 1, "")
    
    
    
    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_get_path_attributes(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for get_county_attributes()
    """
    if len(computed) != len(expected):
        msg = "computed length = " + str(len(computed)) + ", expected length = " + str(len(expected))
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
        return False
    return True
    
    
    
def check_get_d_verts(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for get_boundary_vertices()
    """
        
    computed_array = np.array(computed)
    expected_array = np.array(expected)
    
    if not computed_array.shape == expected_array.shape:
        msg = "computed shape = " + str(computed_array.shape) + ", expected shape = " + str(expected_array.shape)
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False    
    
    if not np.allclose(computed_array, expected_array):
        msg = "computed vertices = " + str(computed) + ", expected vectices = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0.1, msg)
        return False
    return True


def check_make_centers_df(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for make_county_dataframe()
    """
    passed, partial, msg = compare_df(computed, expected)
    if not passed:
        ct.failed_large(fun_name, idx, fun_pts, partial, msg)
    return passed


# Import test cases and test against student solutions using checker functions

CHECKER_DICT = {"get_path_attributes" : (check_get_path_attributes, 10),
                "get_d_verts" : (check_get_d_verts, 10),
                "make_centers_df" : (check_make_centers_df, 10)}                

ct.run_checkers("project8", CHECKER_DICT)





