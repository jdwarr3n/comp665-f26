"""
Unified testing code for all projects in Data Visualization
"""

import sys
import copy
import dill as pickle
import importlib

sys.path.append("../")

class ProjectTests:
    """
    Class for creating, saving, loading, and checking tests for projects
    """
    
    def __init__(self, fun_names, record_tests=False):
        """
        Input: List fun_names of string, optional Boolean record_tests
        
        Output: ProjectTests object containing dictionary of test cases
        keyed by fun_name
        """
        
        self.test_cases = {}
        for name in fun_names:
            self.test_cases[name] = []
            
        self.record_tests = record_tests
        self.pause_add_test = 0
    
    def add_test(self, fun_name, test_case):
        """
        Input: string fun_name, input/output pair test_case
        
        Action: Append test_case to corresponding entry in test case dictionary
        """
        
        if self.record_tests and self.pause_add_test == 0:
            self.test_cases[fun_name].append(copy.deepcopy(test_case))
    
    def pause_tests(self):
        """        
        Action: Pausing recording of tests via add_test()
        
        Note that multiple pause_tests() stack
        """
        
        self.pause_add_test += 1
        
    
    def resume_tests(self):
        """        
        Action: Resume recording of tests via add_test()
        
        Note that multiple resume_tests() clear stacked pause_tests()
        """
        
        self.pause_add_test -= 1        


    def save_tests(self, project_name):
        """
        Input: string project_name
        
        Action: Save test cases for project in pickle file
        """

        if self.record_tests:
            for fun_name in self.test_cases:
                print("Generated", len(self.test_cases[fun_name]), "test cases for", fun_name + "()")

            with open(project_name, 'wb') as file:
                pickle.dump(self, file)        
    
    def check_tests(self, student, checker_dict):
        """
        Input: module student, dictionary of functions checker_dict
        
        Action: Run checker functions in checker_dict on corresponding test cases
        """
        
        for fun_name in checker_dict:
            print("\nChecking", fun_name + "() on", len(self.test_cases[fun_name]), "test cases")
            ok = True
            (fun_checker, fun_pts) = checker_dict[fun_name]
            for idx, test_case in enumerate(self.test_cases[fun_name]):
                inputs, expected = test_case
                try:
                    fun_def = getattr(student, fun_name)
                    computed = fun_def(*inputs)
                except Exception as err:
                    failed_large(fun_name, idx, fun_pts, 0, "Test call raised exception: " + repr(err))
                    ok = False
                    break
                try:
                    ok = fun_checker(computed, expected, inputs, idx, fun_name, fun_pts)
                except Exception as err:
                    failed_large(fun_name, idx, fun_pts, 0, "Checker call raised exception: " + repr(err))
                    ok = False
                    break                    
                
                if not ok:
                    break
            if ok:
                passed(fun_name, fun_pts)

    
    
##################################################################
# Run all tests using test cases

TESTS_PATH = "data/"

def run_checkers(project_name, checker_dict):
    """
    Input: String project_name, dictionary check_dict
    
    Action: Read in test cases for given project and run all checker functions
    in checker_dict on these test cases using functions in student
    """
    try:
        student = importlib.import_module(project_name + "_solution")
    except Exception as err:
        print("Exception when importing student solution: " + repr(err))
        print("Double check that cells with calls to testing/plotting code have the tag \"notebook_only\".\n")
    else:    
        total_score = sum([checker_dict[fun_name][1] for fun_name in checker_dict])
        print("Testing correctness for " + project_name + "_solution.py, maximum score is " + str(total_score) + " points")

        with open(TESTS_PATH + project_name + "_tests.pickle", 'rb') as file:
            # Weird error in Project 14 using dill with classes that appeared recently
            # https://stackoverflow.com/questions/42960637/python-3-5-dill-pickling-unpickling-on-different-servers-keyerror-classtype
            pickle._dill._reverse_typemap['ClassType'] = type
            project_tests = pickle.load(file)
        project_tests.check_tests(student, checker_dict)



##################################################################
# Helper functions for reporting test results

def passed(fun_name, fun_pts):
    """
    Input: String fun_name, integer fun_score
    
    Action: Print appropriate messages to stdout and stderr
    for passing all test for specified function
    """
    print(fun_name + "() PASSED all tests, (" + str(fun_pts) + "/" + str(fun_pts) + " pts)")
    if fun_pts > 0:
        print(fun_name + ", " + str(fun_pts), file=sys.stderr)
      
    
def failed_small(fun_name, inputs, fun_pts, partial, msg):
    """
    Input: String fun_name, tuple inputs, integer fun_pts, float partial, string msg
    
    Action: Print appropriate messsges to stdout and stderr
    for fail a test for for speficied function
    Used for function calls that have small inputs
    """
    fun_args = "("
    for input in inputs:
        if isinstance(input, str):
            fun_args += "'" + str(input) + "', "
        else:
            fun_args += str(input) + ", "
    fun_args = fun_args[:-2] + ")"
    
    fun_score = round(fun_pts * partial)
    print(fun_name + fun_args + " FAILED test, " + msg +
          ", (" + str(fun_score) + "/" + str(fun_pts) + " pts)")
    if fun_pts > 0:
        print(fun_name + ", " + str(fun_score), file=sys.stderr)


def failed_large(fun_name, idx, fun_pts, partial, msg):
    """
    Input: String fun_name, integer fun_pts, float partial, string msg
    
    Action: Print appropriate messsges to stdout and stderr
    for fail a test for for speficied function
    Used for function calls that have large inputs    
    """
    fun_score = round(fun_pts * partial)
    print(fun_name + "()" + " FAILED on test case " + str(idx) + ", " + msg +
          ", (" + str(fun_score) + "/" + str(fun_pts) + " pts)")
    if fun_pts > 0:
        print(fun_name + ", " + str(fun_score), file=sys.stderr)
    
    

