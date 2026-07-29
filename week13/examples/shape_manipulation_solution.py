"""
Solution for week 13 practice in Data Visualization

Converting between 1D and 2D arrays/lists
"""


import numpy as np

TEST_SHAPE = (3, 5)
TEST_FUN = lambda i, j: i + 3 * j

def numpy_shape_manipulations():
    """ Examples of converting between 1D and 2D arrays """

    # Create a 2D test array
    original = np.fromfunction(TEST_FUN, TEST_SHAPE, dtype=int)
    print(original)

    # Stored in 1D form using row major order
    flattened = original.ravel()
    print(flattened)

    # Return to 2D form
    restored = flattened.reshape(TEST_SHAPE)
    print(restored)

    # Select item in original 2D array
    original_index = (1, 4)
    print(original[original_index])

    # Select corresponding item in flattened 1D array
    flattened_index = np.ravel_multi_index(original_index, TEST_SHAPE)
    print(flattened_index, flattened[flattened_index])
    
    # Selecting corresponding item in restored 2D array
    restored_index = np.unravel_index(flattened_index, TEST_SHAPE)
    print(restored_index, restored[restored_index])

numpy_shape_manipulations()
    

# Write equivalent Python list operations for 1D lists <-> 2D table

def make_list(table):
    """
    Input: 2D lists of lists table
    
    Output: Flattened 1D list consisting rows of the table
    """
    return [item for row in table for item in row]

def make_table(flat_list, shape):
    """
    Input: 1D list flat_list, tuple shape of two integers
    
    Output: 2D lists of lists whose rows are of length shape[1]
    """
    return [flat_list[row * shape[1] : (row + 1) * shape[1]] for row in range(shape[0])]

def list_index(table_index, shape):
    """
    Input: tuple table_index of two integers, tuple shape of two integers
    
    Output: integer
    """
    return table_index[0] * shape[1] + table_index[1]

def table_index(list_index, shape):
    """
    Input: integer list_index, tuple shape of two integers
    
    Output: tuple of two integers
    """
    return (list_index // shape[1], list_index % shape[1])


def list_shape_manipulations():
    
    original = [[TEST_FUN(i, j) for j in range(TEST_SHAPE[1])] for i in range(TEST_SHAPE[0])]
    print(original)
    
    flattened = make_list(original)
    print(flattened)

    restored = make_table(flattened, TEST_SHAPE)
    print(restored)
    
    original_index = (1, 4)
    print(original_index, original[original_index[0]][original_index[1]])

    # Select corresponding item in flattened 1D array
    flattened_index = list_index(original_index, TEST_SHAPE)
    print(flattened_index, flattened[flattened_index])
    
    # Selecting corresponding item in restored 2D array
    restored_index = table_index(flattened_index, TEST_SHAPE)
    print(restored_index, restored[restored_index[0]][restored_index[1]])    
    
    
#list_shape_manipulations()

