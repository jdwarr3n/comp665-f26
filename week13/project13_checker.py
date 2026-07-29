"""
Testing code for Project 13

Student will implement the following functions:

make_quads(grid_shape)
make_trimesh_fixed(z_grid, diagonal)
make_trimesh_feature(z_grid)
"""

import numpy as np
import sys
sys.path.append('../public')
import common_testing as ct
# New: for importing the project code
import sys;sys.modules['common_testing.common_testing'] = ct

######################################################################
# Helper functions for comparing 2D arrays of tri/quad vertex indices

def ordered(poly):
    """
    Input: Tuple poly of integer vertex indices
    
    Output: Sorted tuple consisting of these indices
    """
    return tuple(sorted(poly))

def set_of_ordered_tuples(polys):
    """
    Input: 2D numpy array polys whose rows are the indices for a polygonal mesh
    
    Output: Set of ordered tuples for rows of poly
    """
    
    answer = set([])
    for poly in polys:
        answer.add(tuple(sorted(poly)))
    return answer

    
    
#########################################################################
# Test case checkers for each machine-graded function in project
    
def check_make_quads(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for make_quads()
    """
    if type(computed) != type((1, )) or len(computed) != 2:
        msg = " computed is not a tuple of length 2"
        ct.failed_small(fun_name, inputs, fun_pts, 0, msg)
        return False
    if not np.array_equal(computed[0], expected[0]):
        msg = "computed[0] is " + str(computed[0]) + ", expected[0] is " + str(expected[0])
        ct.failed_small(fun_name, inputs, fun_pts, 0.2, msg)
        return False
    if len(computed[1]) != len(expected[1]):
        msg = "Computed mesh has " + str(len(computed[1])) + " quads while expected mesh has " + str(len(expected[1])) + " quads"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    
    computed_quad_set = set_of_ordered_tuples(computed[1])
    for quad in expected[1]:
        if ordered(quad) not in computed_quad_set:
            msg = "Expected quad with indices " + str(quad) + " does not appear in quads computed"
            ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
            return False
    return True
    


def check_make_trimesh_fixed(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for make_trimesh_fixed()
    """
    if type(computed) != type((1, )) or len(computed) != 2:
        msg = "computed is not a tuple of length 2"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if not np.array_equal(computed[0], expected[0]):
        msg = "vertices of computed and expected disagree"
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False
    if len(computed[1]) != len(expected[1]):
        msg = "Computed mesh has " + str(len(computed[1])) + " triangles while expected mesh has " + str(len(expected[1])) + " triangles"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
    
    computed_tri_set = set_of_ordered_tuples(computed[1])
    for tri in expected[1]:
        if ordered(tri) not in computed_tri_set:
            msg = "Expected triangle with indices " + str(tri) + " does not appear in triangles for computed"
            ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
            return False
    return True



def check_make_trimesh_feature(computed, expected, inputs, idx, fun_name, fun_pts):
    """
    Check a specific test case for make_trimesh_feature()
    
    Note expected may include quads.  This output is by design and
    models situations where either triangulation of the quad is be acceptable
    """

    if type(computed) != type((1, )) or len(computed) != 2:
        msg = "computed is not a tuple of length 2"
        ct.failed_large(fun_name, idx, fun_pts, 0, msg)
        return False
    if not np.array_equal(computed[0], expected[0]):
        msg = "vertices of computed and expected disagree"
        ct.failed_large(fun_name, idx, fun_pts, 0.1, msg)
        return False
    
    computed_tri_set = set_of_ordered_tuples(computed[1])
    expected_tri_num = 0
    for poly in expected[1]:
        if len(poly) == 3:
            expected_tri_num += 1
            if ordered(poly) not in computed_tri_set:
                msg = "Expected triangle with indices " + str(poly) + " does not appear in triangles for computed"
                ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
                return False
        else:
            expected_tri_num += 2
            tri0 = ordered((poly[0], poly[1], poly[2])) 
            tri1 = ordered((poly[2], poly[3], poly[0]))
            tri2 = ordered((poly[1], poly[2], poly[3]))
            tri3 = ordered((poly[3], poly[0], poly[1]))
            if not ((tri0 in computed_tri_set and tri1 in computed_tri_set) or
                    (tri2 in computed_tri_set and tri3 in computed_tri_set)):
                msg = "Pair of computed triangles for quad with indices " + str(poly) + " do not appear in triangles for computed"
                ct.failed_large(fun_name, idx, fun_pts, 0.4, msg)
                return False
            
    if len(computed[1]) != expected_tri_num:
        msg = "Computed mesh has " + str(len(computed[1])) + " triangles while expected mesh has " + str(expected_tri_num) + " triangles"
        ct.failed_large(fun_name, idx, fun_pts, 0.2, msg)
        return False
            
    return True        





# Import test cases and test against student solutions using checker functions

CHECKER_DICT = {"make_quads" : (check_make_quads, 10),
                "make_trimesh_fixed" : (check_make_trimesh_fixed, 10), 
                "make_trimesh_feature" : (check_make_trimesh_feature, 10)}                

ct.run_checkers("project13", CHECKER_DICT)


