"""
Template for week 7 practice of Data Visualization

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
        
        return 0.0
        
    return quad_fun
        
        

def test_quad_minimize():
    """
    Action: Creates a quadratic function with a random minimum,
    Uses scipy.optimize to compute minimum,
    Verifies that two quantites are all equal.
    """
    
    SIZE = 20
    
    # Create a numpy array exoected of given SIZE with random numbers
    
    # Create a quadratic function quad_fun with these values as its minimum

    # Create a random initial guess init
    
    # Compute the minimum of quad_fun using opt.minimize() using init
    
    # Test whether computed and expected minimums agree

test_quad_minimize()







