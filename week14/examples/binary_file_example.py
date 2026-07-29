"""
Examples of writing and read a binary file for 2D array using the struct module
https://docs.python.org/3/library/struct.html

A binary file is one whose format is understood in advance
"""


import struct
import numpy as np


def write_table(table, file_name):
    """
    Input: 2D numpy array table of unints, string file_name
    
    Action: Write binary file filename with following format:
    2 integers corresponding to shape of array followed by
    1D array of unint8 generated from 2D array
    """
        
    # Flatten the table and write its shape/contents to a string
    flat_table = np.ravel(table)
    
    # Prepare the format string, includes shape and contents of table
    table_fmt = "=2i" + str(len(flat_table)) + "B"
    print("Packing array with format string is", table_fmt)
    
    # Pack the shape and contents of the table, remmeber that *seq unpacks sequence seq
    packed_table = struct.pack(table_fmt, *table.shape, *flat_table)  
    
    # Write the string to a binary file
    with open(file_name, "wb") as table_file:
        table_file.write(packed_table)
    
def read_table(file_name):
    """
    Input: string file_name
    
    Output: 2D numpy array stored in binary format in file filename
    """
    with open(file_name, "rb") as table_file:
        table_binary = table_file.read()
        
    shape_fmt = "=2i"
    table_shape = struct.unpack_from(shape_fmt, table_binary)
    print("Read shape", table_shape)
      
    table_size = table_shape[0] * table_shape[1]
    table_offset = struct.calcsize(shape_fmt)
    table_fmt = "=" + str(table_size) + "B"
    
    table_bytes = struct.unpack_from(table_fmt, table_binary, table_offset)
    flat_table = np.array(table_bytes, dtype=np.uint8)
    return np.reshape(flat_table, table_shape)

def test_binary_methods():
    
    SHAPE = (5, 10)
    FILE_NAME = "table.bin"
    
    table = np.random.randint(256, size=SHAPE, dtype=np.uint8)
    print("Defining 2D table of type", table.dtype, "with shape", SHAPE)
    print(table)
    
    print("Writing table in binary format as file", FILE_NAME)
    write_table(table, FILE_NAME)
    # Note that file contains exactly 58 bytes
    
    print()
    print("Reading file", FILE_NAME, "in binary format")
    new_table = read_table(FILE_NAME)
    print(new_table)
    
    print("Comparing original and saved table")
    print("Comparison of table types is", table.dtype == new_table.dtype)
    print("Comparison of table contents is", np.array_equal(table, new_table))
    
test_binary_methods()