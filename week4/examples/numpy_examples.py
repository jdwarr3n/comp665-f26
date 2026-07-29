"""
Simple examples of numpy in action
"""

import numpy as np

# 1D arrays

# array method converts list to numpy array  
array1 = np.array([0, 3, 7, 12, 18])
print("array1 is", array1)

# Create an array of 5 equally spaced numbers from 0 to 20  
array2 = np.linspace(0.0, 20.0, 5)
print("array2 is", array2)

# Get the data type of array2
print("The data type of array2 is", array2.dtype)

# Create an array similar to array2 including integers 
array3 = np.linspace(0., 20., 5, dtype=int)
print("array3 is", array3)
print("The data type of array3 is", array3.dtype)

# Select from 1D array by passing an index or a slice
print(array1[2])
print(array3[1:-1])

# Arithmetic operations applied to arrays  
print("array1 + array3 equals\n", array1 + array3)
print("array2 * 3 equals\n", array2 * 3)


# 2D arrays

# Simple example of 2D array
array4 = np.array([[0, 1, 2], [4, 5, 6]])
print("2D example array\n", array4)

# Note 2D arrays are indexed by (row, col)
print("Entry (1, 0) of array4 is", array4[1, 0])

# Array's shape is number of rows by number of columns
num_rows, num_cols = array4.shape
print("Shape of array4 is", (num_rows, num_cols)) 


# Build a grid of (x, y) coordinates that correspond to row/col position of elements in array4
x_coords = np.linspace(0, num_cols - 1, num_cols)
y_coords = np.linspace(0, num_rows - 1, num_rows)
print("x coordinates are", x_coords)
print("y coordinates are", y_coords)

x_grid, y_grid = np.meshgrid(x_coords, y_coords)
print("Grid of x coordinates is\n", x_grid)
print("Grid of y coordinates is\n", y_grid)

print("(x, y) position of array[1, 0] is", x_grid[1, 0], y_grid[1, 0])
# Note that array are indexed by row/col, but points are position by (x, y)
# Here, row corresponds to y coordinate, col correspond to x
# Origin is in upper left

# Compute the transpose of a 2D numpy array 
print("Transpose of x_grid is\n", x_grid.T)
