"""
Testing code for Project 7

Student will implement the following functions:

make_graph(nodes, edges, name=None)
random_layout(grph, range=[-1, 1, -1, 1], seed=None)
get_node_indices(grph)
distance_error(node_pos, distances)
distance_layout(grph, seed=1)
get_communities(grph)
"""


import random
import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
sys.modules['common_testing.common_testing'] = ct

DISTANCE_TOL = 0.000001
LAYOUT_TOL = 0.025

    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_make_graph(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for make_graph()
    """
    if computed.nodes() != expected.nodes():
        msg = "computed nodes = " + str(computed.nodes()) + ", expected nodes =" + str(expected.nodes())
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    if computed.edges() != expected.edges():
        msg = "computed edges =" + str(computed.edges()) + ", expected edges = " + str(expected.edges())
        ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
        return False
    if computed.name != expected.name:
        msg = "computed.name = " + str(computed.name) + ", expected.name = " + str(expected.name)
        ct.failed_small(fun_name, inputs, fun_pts, 0.4, msg)
        return False
    return True
    
    
    
def check_random_layout(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for random_layout()
    """
    if set(computed.keys()) != set(expected.keys()):
        msg = "computed keys = " + str(computed.keys()) + ", expected keys = " + str(expected.keys())
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    for key in computed.keys():
        if not np.allclose(np.array(computed[key]), np.array(expected[key])):
            msg = "computed[" + str(key) + "] = " + str(computed[key]) + ", expected[" + str(key) + "] = " + str(expected[key])
            ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
            return False
    return True


def check_get_node_indices(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for get_path_lengths()
    """
    if set(computed.keys()) != set(expected.keys()):
        msg = "computed keys = " + str(computed.keys()) + ", expected keys = " + str(expected.keys())
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    for node in computed.keys():
        if computed[node] != expected[node]:
            msg = "computed[" + str(node) + "] = " + str(computed[node]) + ", expected[" + str(node) + "] = " + str(expected[node])
            ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
            return False
    return True

def check_distance_error(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for distance_error()
    """
    if abs(computed - expected) > DISTANCE_TOL:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    return True
    
    
def check_distance_layout(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for distance_layout()
    """
    if set(computed.keys()) != set(expected.keys()):
        msg = "computed keys = " + str(computed.keys()) + ", expected keys = " + str(expected.keys())
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    for key in computed.keys():
        if not np.allclose(np.array(computed[key]), np.array(expected[key]), atol=LAYOUT_TOL):
            msg = "computed[" + str(key) + "] = " + str(computed[key]) + ", expected[" + str(key) + "] = " + str(expected[key])
            ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
            return False
    return True



def check_get_communities(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for get_communities()
    """
    if computed != expected:
        msg = "computed = " + str(computed) + ", expected = " + str(expected)
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    return True

    


# Import test cases and test against student solutions using checker functions

CHECKER_DICT = {"make_graph" : (check_make_graph, 0),
                "random_layout" : (check_random_layout, 0),
                "get_node_indices" : (check_get_node_indices, 7),
                "distance_error" : (check_distance_error, 7),
                "distance_layout" : (check_distance_layout, 10),
                "get_communities" : (check_get_communities, 6)}                

ct.run_checkers("project7", CHECKER_DICT)

