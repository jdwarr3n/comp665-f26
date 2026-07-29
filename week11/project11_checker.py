"""
Testing code for Project 11

Student will implement the following functions:

kmeans_clustering(cluster_list, num_clusters, num_iterations)
"""

import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys;sys.modules['common_testing.common_testing'] = ct


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
# Test case checkers for each machine-graded function in project 11
    
def check_kmeans_clustering(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for kmeans_clustering()
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
            msg =  "expected cluster " + str(expected_cluster) + " not in computed clustering " + str(computed_clusters)
            ct.failed_large(fun_name, idx, fun_pts, 0, msg)    
            return False
    return True
    



# Import test cases and test against student solutions using checker functions

CHECKER_DICT = {"kmeans_clustering" : (check_kmeans_clustering, 20)}                

ct.run_checkers("project11", CHECKER_DICT)





