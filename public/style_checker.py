"""
Pylint style checker for Data Visualization

Uses py_run from pylint.epylint
"""

import sys, os
import pylint.epylint as lint

# Constants
MAX_SCORE = 10

# Relative path in single pylintrc file
#CONFIG_PATH = "./"                             # Regular tests
#CONFIG_PATH = "\\..\\grading\\pylint\\"         # Weekly project scripts on Dropbox on Windows
CONFIG_PATH = "/../public/"   # Vocareum

def run_pylint(file_name, max_score=MAX_SCORE):
    """
    Input: String file_name, optional int max_score
    
    Output: Prints formmated results of running pylint on file file_name
    Messages are printed to stdout, score is printed to stderr
    """
    print("\nTesting style for " + file_name + ", maximum score is " + str(max_score) + " points")
    print()
    
    if not os.path.isfile(file_name):
        print("File " + file_name + " not found, no score reported")
        return
    
    options = ' --rcfile=' + os.getcwd() + CONFIG_PATH + "pylintrc"
    msg_template = "Line={line}:[{msg_id}]{msg}"
    options += " --msg-template=" + msg_template
    
    pylint_stdout, pylint_stderr = lint.py_run(file_name + options, return_std=True)
    process_pylint_output(pylint_stdout, pylint_stderr, max_score)
    


def process_pylint_output(pylint_stdout, pylint_stderr, max_score):
    """
    Input: files pylint_stdout, pylint_stderrr, int max_score
    
    Action: Prints formatted contents of pylint_stdout to stdout
    if stderr is empty
    """
    
    err_msgs = pylint_stderr.getvalue()
    if err_msgs != "":
        print("Pylint encountered the following error:")
        print(err_msgs)
        print()
        print("Style score is 0/10 pts")
        print("style, " + str(0), file=sys.stderr)
    else:
        current_score = max_score
        print("Pylint detected the following issues:")
        out_msgs = pylint_stdout.getvalue()
        out_lines = out_msgs.split("\n")
        for line in out_lines:
            if line[1 : 5] == "Line":
                print(line[1:] + " (-1 pt)")
                current_score -= 1
        final_score = max(0, current_score)
        print("\nStyle score is " + str(final_score) + "/" + str(max_score) + " pts")
        print("style, " + str(final_score), file=sys.stderr)
    return   
    

## Desktop
##run_pylint("../../week5/project5_solution.py")

## Command line
if __name__ == '__main__':
    if len(sys.argv) == 2:
        run_pylint(sys.argv[1])
    else:
        run_pylint(sys.argv[1], int(sys.argv[2]))
