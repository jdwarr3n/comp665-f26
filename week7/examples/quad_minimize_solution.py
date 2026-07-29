"""
Solution for week 7 practice of Data Visualization

Use scipy.optimize to compute the minimum of a quadratic function
"""


import random
import numpy as np
import scipy.optimize as opt


def make_quad_fun(minimum):
    """
    Input: numpy array minimum of floats
    
    Output: spherical function with given minimum
    """
    
    def quad_fun(vals):
        return sum((vals - minimum) ** 2)
    return quad_fun
        
        

def test_quad_minimize():
    """
    Action: Creates a quadratic function with a random minimum,
    Uses scipy.optimize to compute minimum,
    Verifies that two quantites are all equal.
    """
    
    SIZE = 20
    expected = np.array([random.random() for i in range(SIZE)])
    print("Expected minima are", expected)
    print()
    
    quad_fun = make_quad_fun(expected)
    init = [random.random() for i in range(SIZE)]
    computed = opt.minimize(quad_fun, init).x
    print("Computed minima are", computed)
    print()
    print("expected == computed is", np.allclose(expected, computed))

test_quad_minimize()







