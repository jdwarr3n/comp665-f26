"""
An example of finding the solution to a quadratic equation
"""




import numpy as np
import math


# Arithmetic operations on complex numbers
x = 1 + 2j
y = complex(3, -2)

print("Do some complex arithmetic")
print(x + y)
print(x * y)
print(x / y)

# Use poly1d module
quad = np.poly1d((1, 0, 4))

print()
print("Work with poly1d from numpy")
print("Poly is\n", quad)
print("Roots are", quad.r)
print("Derivative is", quad.deriv())


# compute complex number via  polar form

def polar(radius, theta):
    """
    Input: floats radius, theta
    Output: complex number associate with polar form of (radius, theta)
    """
    
    return complex(radius * math.cos(theta), radius * math.sin(theta))

# Experiment with squares in complex forms

def sqr_test():
    """
    Example of square computation in polar form
    """
    print()
    rad = 2.3
    theta = math.pi / 3
    
    
    # Define complex number in polar form
    z = polar(rad, theta)
    print(z)
    print(z ** 2)
    print(polar(rad ** 2, 2 * theta))
    
sqr_test()


# Experiment with square roots in complex form

def sqr_root_test():
    """
    Example of square root computation in polar form
    """
    print()
    rad = 2.3
    theta = math.pi / 3
    
    # Define complex number in polar form
    z = polar(rad, theta)
    print(z)
    
    # Compute one square root and square it
    plus_sqr_z = polar(math.sqrt(rad), theta / 2)
    print(plus_sqr_z ** 2)
    
    
    # Compute other square root and square it
    neg_sqr_z = polar(math.sqrt(rad), theta / 2 + math.pi)
    print(neg_sqr_z ** 2)

sqr_root_test()


