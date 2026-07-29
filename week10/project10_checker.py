"""
Testing code for Project 10

Student will implement the following functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
"""

import random
import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys;sys.modules['common_testing.common_testing'] = ct

################################################################
# Answers for small closest pairs tests, handles multiple minima


SMALL_SLOW_CLOSEST_PAIRS = [set([(1.0, 0, 1)]),
                       set([(0.806225774829855, 0, 1)]),
                       set([(1.0, 1, 2), (1.0, 0, 1)]),
                       set([(1.4142135623730951, 0, 1)]),
                       set([(1.4142135623730951, 1, 2), (1.4142135623730951, 0, 1)]),
                       set([(1.0, 2, 3), (1.0, 1, 2), (1.0, 0, 1)]),
                       set([(1.0, 2, 3), (1.0, 1, 2), (1.0, 0, 1)]),
                       set([(1.0, 1, 3), (1.0, 0, 2), (1.0, 2, 3), (1.0, 0, 1)]),
                       set([(1.0, 0, 3), (1.0, 5, 8), (1.0, 4, 7), (1.0, 3, 6), (1.0, 6, 7), (1.0, 1, 2), (1.0, 4, 5), (1.0, 2, 5), (1.0, 3, 4), (1.0, 0, 1), (1.0, 1, 4), (1.0, 7, 8)]),
                       set([(1.0, 1, 2)]),
                       set([(1.0, 1, 2)]),
                       set([(0.14212670403551897, 1, 3)]),
                       set([(0.26, 0, 1)]),
                       set([(0.2209072203437452, 1, 4)]),
                       set([(0.08944271909999157, 1, 4)]),
                       set([(0.10440306508910548, 0, 2)]),
                       set([(0.06999999999999995, 0, 1)]),
                       set([(0.3014962686336267, 1, 3)]),
                       set([(0.08944271909999157, 0, 3)]),
                       set([(0.06403124237432847, 0, 1)]),
                       set([(0.17464249196572987, 0, 2)]),
                       set([(0.028284271247461926, 0, 2)]),
                       set([(2.0, 1, 2)]),
                       set([(2.0, 0, 5)]),
                       set([(0.2, 2, 3)]),
                       set([(0.3026549190084311, 3, 4)]),
                       set([(0.08944271909999157, 2, 4)]),
                       set([(0.10440306508910548, 0, 1)]),
                       set([(0.07615773105863904, 3, 4)]),
                       set([(0.2, 0, 1), (0.2, 3, 4)])]


SMALL_FAST_CLOSEST_PAIRS = [set([(1.0, 0, 1)]),
                       set([(0.806225774829855, 0, 1)]),
                       set([(1.0, 1, 2), (1.0, 0, 1)]),
                       set([(1.4142135623730951, 0, 1)]),
                       set([(1.4142135623730951, 1, 2), (1.4142135623730951, 0, 1)]),
                       set([(1.0, 2, 3), (1.0, 1, 2), (1.0, 0, 1)]),
                       set([(1.0, 2, 3), (1.0, 1, 2), (1.0, 0, 1)]),
                       set([(1.0, 1, 3), (1.0, 0, 2), (1.0, 2, 3), (1.0, 0, 1)]),
                       set([(1.0, 0, 3), (1.0, 5, 8), (1.0, 4, 7), (1.0, 3, 6), (1.0, 6, 7), (1.0, 1, 2), (1.0, 4, 5), (1.0, 2, 5), (1.0, 3, 4), (1.0, 0, 1), (1.0, 1, 4), (1.0, 7, 8)]),
                       set([(1.0, 1, 2)]),
                       set([(1.0, 1, 2)]),
                       set([(0.14212670403551897, 0, 1)]),
                       set([(0.26, 0, 1)]),
                       set([(0.2209072203437452, 0, 1)]),
                       set([(0.0894427191, 1, 4)]),
                       set([(0.104403065089, 0, 2)]),
                       set([(0.06999999999999995, 2, 3)]),
                       set([(0.3014962686336267, 3, 4)]),
                       set([(0.08944271909999157, 1, 2)]),
                       set([(0.06403124237432847, 1, 2)]),
                       set([(0.17464249196572987, 2, 4)]),
                       set([(0.028284271247461926, 3, 4)]),
                       set([(2.0, 1, 2)]),
                       set([(2.0, 0, 5)]),
                       set([(0.2, 2, 3)]),
                       set([(0.3026549190084311, 0, 3)]),
                       set([(0.08944271909999157, 1, 4)]),
                       set([(0.10440306508910548, 0, 2)]),
                       set([(0.07615773105863904, 3, 4)]),
                       set([(0.2, 0, 1), (0.2, 3, 4)])]

SMALL_STRIP_PAIRS = [set([(1.0, 1, 2)]),
                       set([(1.0, 1, 2), (1.0, 0, 1), (1.0, 2, 3)]),
                       set([(1.0, 1, 3), (1.0, 0, 2), (1.0, 0, 1), (1.0, 2, 3)]),
                       set([(1.0, 4, 7), (1.0, 5, 8), (1.0, 0, 3), (1.0, 3, 6), (1.0, 3, 4), (1.0, 4, 5), (1.0, 1, 4), (1.0, 6, 7), (1.0, 7, 8), (1.0, 1, 2), (1.0, 0, 1), (1.0, 2, 5)]),
                       set([(1.0, 1, 2)]),
                       set([(1.0, 1, 2)]),
                       set([(0.16970562748477142, 1, 2)]),
                       set([(0.26, 0, 1)]),
                       set([(0.25059928172283336, 2, 3)]),
                       set([(0.0894427191, 1, 4)]),
                       set([(float('inf'), -1, -1)]),
                       set([(float('inf'), -1, -1)]),
                       set([(0.3014962686336267, 3, 4)]),
                       set([(0.08944271909999157, 1, 2)]),
                       set([(0.06403124237432847, 1, 2)]),
                       set([(0.3966106403010388, 1, 2)]),
                       set([(0.25179356624028343, 1, 2)]),
                       set([(2.0, 1, 2)]),
                       set([(2.0, 0, 5)]),
                       set([(0.2, 2, 3)]),
                       set([(0.3026549190084311, 0, 3)]),
                       set([(0.08944271909999157, 1, 4)]),
                       set([(float("inf"), -1, -1)]),
                       set([(float("inf"), -1, -1)]),
                       set([(float("inf"), -1, -1)])]


#######################################################
# Helper function for comparing two clusterings

def set_of_county_tuples(cluster_list):
    """
    Input: A list of Cluster objects
    Output: Set of sorted tuple of counties corresponds to counties in each cluster
    """
    set_of_clusters = set([])
    for cluster in cluster_list:
        counties_in_cluster = cluster.fips_codes()
        
        # convert to immutable representation before adding to set
        county_tuple = tuple(sorted(list(counties_in_cluster)))
        set_of_clusters.add(county_tuple)
    return set_of_clusters
    

    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_slow_closest_pair(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for slow_closest_pair()
    """

    if idx < len(SMALL_SLOW_CLOSEST_PAIRS):
        for pair in SMALL_SLOW_CLOSEST_PAIRS[idx]:
            if np.allclose(np.array(computed), np.array(pair)):
                return True
        msg = "computed = " + str(computed) + ", expected should be in " + str(SMALL_SLOW_CLOSEST_PAIRS[idx])
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    else:
        if not np.allclose(np.array(computed), np.array(expected)):
            msg = "please email the instructors a copy of your code for further inspection"
            ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
            return False
    return True
    
    
    
def check_fast_closest_pair(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for fast_closest_pair()
    """
    
    if idx < len(SMALL_FAST_CLOSEST_PAIRS):
        for pair in SMALL_FAST_CLOSEST_PAIRS[idx]:
            if np.allclose(np.array(computed), np.array(pair)):
                return True
        msg = "computed = " + str(computed) + ", expected should be in " + str(SMALL_FAST_CLOSEST_PAIRS[idx])
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    else:
        if not np.allclose(np.array(computed), np.array(expected)):
            msg = "please email the instructors a copy of your code for further inspection"
            ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)            
            return False
    return True


def check_closest_pair_strip(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for closest_pair_strip()
    """
    
    if idx < len(SMALL_STRIP_PAIRS):
        for pair in SMALL_STRIP_PAIRS[idx]:
            if np.allclose(np.array(computed), np.array(pair)):
                return True
        msg = "computed = " + str(computed) + ", expected should be in " + str(SMALL_STRIP_PAIRS[idx])
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    else:
        if not np.allclose(np.array(computed), np.array(expected)):
            msg = "please email the instructors a copy of your code for further inspection"
            ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)      
            return False
    return True


def check_hierarchical_clustering(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for hierarchical_clustering()
    """
    computed_clusters = set_of_county_tuples(computed)
    expected_clusters = set_of_county_tuples(expected)
    for computed_cluster in computed_clusters:
        if computed_cluster not in expected_clusters:
            msg = "computed cluster " + str(computed_cluster) + " not in expected clustering " + str(expected_clusters)
            ct.failed_large(fun_name, idx, fun_pts, 0, msg) 
            return False
    for expected_cluster in expected_clusters:
        if expected_cluster not in computed_clusters:
            msg = "expected cluster " + str(expected_cluster) + " not in computed clustering " + str(computed_clusters)
            ct.failed_large(fun_name, idx, fun_pts, 0, msg) 
            return False
    return True



# Import test cases and test against student solutions using checker functions

CHECKER_DICT = {"slow_closest_pair" : (check_slow_closest_pair, 10),
                "fast_closest_pair" : (check_fast_closest_pair, 10),
                "closest_pair_strip" : (check_closest_pair_strip, 10),
                "hierarchical_clustering" : (check_hierarchical_clustering, 10)}                

ct.run_checkers("project10", CHECKER_DICT)





