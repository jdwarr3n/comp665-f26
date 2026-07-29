"""
Solution for week 3 practice of Data Visualization

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

    item_format = "%-" + str(item_width) + "s"
    with open(file_name, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for item in row:
                print(item_format % item, end="")
            print()


def print_csv_dict(file_name, field_width=12):
    """
    Input: String file_name for CSV file that includes a header row,
    optional integer field_width
    
    Output: List of dictioanaries keyed by the headers,
    output should include left justified fields with fixed width field_width
    """ 
       
    field_format = "%-" + str(field_width) + "s"
    with open(file_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for field in csv_reader.fieldnames:
            print(field_format % field, end="")
        print()
        for row in csv_reader:
            for field in csv_reader.fieldnames:
                print(field_format % row[field], end="")
            print()
        
    
def test_csv_readers():
    """
    Actions: Read a CSV file using read_csv() and print out its contents
    """
    print_csv_list(DATA_PATH + NUMBER_TABLE)
    print_csv_dict(DATA_PATH + NAME_TABLE)

        
test_csv_readers()


