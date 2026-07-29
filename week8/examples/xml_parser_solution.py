"""
Solution for week 8 project in Data Visualization

Parse an attribute-based XML file and return a dictionary of its contents
"""

import xml.dom.minidom as minidom

# Resources
DATA = "../data/"
EMPLOYEE_FILE = "employee_data.xml"

def parse_xml(file_name):
    """
    Input: string file_name
    
    Output: dictionary whose keys are employee ids and whose values are
    dictionarys keyed by first name, last name, and title
    """
    xml_doc = minidom.parse(file_name)     
    employees = {}
    for employee in xml_doc.getElementsByTagName("employee"):
        employee_dict = {}
        employee_id = employee.getAttribute("id")
        employee_dict["first"] = employee.getAttribute("first")
        employee_dict["last"] = employee.getAttribute("last")
        employee_dict["title"] = employee.getAttribute("title")
        employees[employee_id] = employee_dict
    xml_doc.unlink()
    
    return employees

print(parse_xml(DATA + EMPLOYEE_FILE))
    
    