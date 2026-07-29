"""
Template for week 3 practice of Data Visualization

Code to read and print the contents of a CSV file
"""

import csv

# Resource paths
DATA_PATH = "../data/"
NUMBER_TABLE = "number_table.csv"
NAME_TABLE = "name_table.csv"


def print_csv_list(file_name, item_width=5):
    """
    Input: String file_name for CSV file that does not include a header row,
    optional integer item_width
    
    Output: List of list containing the contents of the CSV file,
    output should include left justified items with fixed width item_width
    """ 

    pass    # Implement this function using csv.reader()


def print_csv_dict(file_name, field_width=12):
    """
    Input: String file_name for CSV file that includes a header row,
    optional integer field_width
    
    Output: List of dictioanaries keyed by the headers,
    output should include left justified fields with fixed width field_width
    """ 
       
    pass    # Implement this function using csv.DictReader()
        
    
def test_csv_readers():
    """
    Actions: Read a CSV file using read_csv() and print out its contents
    """
    print_csv_list(DATA_PATH + NUMBER_TABLE)
    print_csv_dict(DATA_PATH + NAME_TABLE)

        
test_csv_readers()


