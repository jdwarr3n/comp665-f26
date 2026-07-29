"""
Testing code for Project 9

Student will implement the following functions:

csv_to_dataframe(file_name, col_idxs, col_names, col_types)
merge_by_column(df1, df2, col_name)
get_high_risk(county_df, num_counties)
"""

import random
import numpy as np
import pandas as pd
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys;sys.modules['common_testing.common_testing'] = ct

INDEX = "FIPS"

def compare_df(df1, df2):
    """
    Input: Dataframes df1, df2 sharing same order sequence of columns
    
    Output: Tuple consisting of boolean, float, string
    Boolean indicates whether two dataframes are equal,
    float is percentagage credit, string is error message
    """
    
    cp1 = df1.copy()
    cp2 = df2.copy()
    
    # Check to see if dataframes have same column names
    col1 = sorted(list(cp1.columns))
    col2 = sorted(list(cp2.columns))
    if col1 != col2:
        msg = "Computed has columns " + str(col1) + ", expected has columns " + str(col2)
        return (False, 0, msg)
    
    # Reorder columns for comparison of dataframes
    cp1 = cp1[col1]
    cp2 = cp2[col2]
    if cp1.shape[0] != cp2.shape[0]:
        msg = "Computed has " + str(cp1.shape[0]) + " rows, expected has " + str(cp2.shape[0]) + " rows"
        return (False, 0.2, msg)
    
    # Set common index
    cp1.set_index(INDEX, inplace=True)
    cp2.set_index(INDEX, inplace=True)
    
    # Check if dataframes have same set of indices
    if set(cp1.index) != set(cp2.index):
        msg = "Computed and expected have differing row indices"
        return (False, 0.3, msg)
    
    # Check if rows corresponding to same index have equal values within tolerance
    for idx in cp1.index:
        if not np.allclose(cp1.loc[idx], cp2.loc[idx]):
            msg = "compute.loc[" + str(idx) + "]  = " + str(list(cp1.loc[idx])) + \
                  ", expected.loc[" + str(idx) + "] = " + str(list(cp2.loc[idx]))
            return (False, 0.4, msg)
    return (True, 1, "")
    

    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_csv_to_dataframe(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for csv_to_dataframe()
    """
    passed, partial, msg = compare_df(computed, expected)
    if not passed:
        ct.failed_small(fun_name, inputs, fun_pts, partial, msg)
    return passed
    
    
    
def check_merge_by_column(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for merge_by_column()
    """
    passed, partial, msg = compare_df(computed, expected)
    if not passed:
        ct.failed_large(fun_name, idx, fun_pts, partial, msg)
    return passed


def check_get_high_risk(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for get_high_risk()
    """
    passed, partial, msg = compare_df(computed, expected)
    if not passed:
        ct.failed_large(fun_name, idx, fun_pts, partial, msg)
    return passed




# Import test cases and test against student solutions using checker functions

CHECK_DICT = {"csv_to_dataframe" : (check_csv_to_dataframe, 10),
              "merge_by_column" : (check_merge_by_column, 10),
              "get_high_risk" : (check_get_high_risk, 10)}                

ct.run_checkers("project9", CHECK_DICT)





