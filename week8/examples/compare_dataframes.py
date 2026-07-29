"""
Code to compare pandas dataframes and give reasonable feedback on differences
https://stackoverflow.com/questions/19917545/comparing-two-pandas-dataframes-for-differences
"""

import numpy as np
import pandas as pd



dict1 = {'col1': ['a', 'b', 'c', 'd'], 'col2': [1, 2, 3, 4], 'col3': [4, 5, 6, 7]}
df1 = pd.DataFrame(data=dict1)

dict2 = {'col1': ['d', 'c', 'b','a'], 'col2': [4, 3, 2, 1], 'col3': [7, 6, 5, 4]}
df2 = pd.DataFrame(data=dict2)

dict3 = {'col1': ['d', 'c', 'b','a'], 'col2': [4, 3, 2, 1], 'col3': [7, 6, 5, 2]}
df3 = pd.DataFrame(data=dict3)

dict4 = {'col2': [4, 3, 2, 1], 'col1': ['d', 'c', 'b','a'], 'col3': [7, 6, 5, 2]}
df4 = pd.DataFrame(data=dict4)


def compare_df(df1, df2, idx):
    """
    Input: Dataframes df1, df2 sharing same order sequence of columns
    Output: Boolean indicating whether two dataframes are equal
    """
    
    cp1 = df1.copy()
    cp2 = df2.copy()
    
    col1 = sorted(list(cp1.columns))
    col2 = sorted(list(cp2.columns))
    
    if col1 != col2:
        print("Dataframes have different columns")
        return False
    
    cp1 = cp1[col1]
    cp2 = cp2[col2]

    if cp1.shape[0] != cp2.shape[0]:
        print("Dataframes have number of rows")
        return False
    
    cp1.sort_values(by=idx, inplace=True)
    cp2.sort_values(by=idx, inplace=True)
    
    compared = (cp1.values == cp2.values)
    if not np.all(compared):
        bad_rows = (np.where(compared == False))[0]
        print("Mismatched rows for index", cp1.values[bad_rows, 0])
        return False
    return True

print(compare_df(df1, df2, "col1"))
print(compare_df(df3, df4, "col1"))
print(compare_df(df1, df3, "col1"))


