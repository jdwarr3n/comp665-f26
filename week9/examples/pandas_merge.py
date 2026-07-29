"""
Examples of merging, joining, and concatenating two dataframes in pandas

https://stackoverflow.com/questions/40468069/merge-two-dataframes-by-index
"""

import pandas as pd

def run_example():
    """ Run an example """
    
    # Define two simple dataframes, note dtype=object prevents converts to float during merge/join/concat
    df1 = pd.DataFrame({'a':range(6), 'b':[5,3,6,9,2,4]}, index=list('abcdef'), dtype=object)
    df2 = pd.DataFrame({'c':range(4), 'd':[10,20,30, 40]}, index=list('abhi'), dtype=object)
    print("First dataframe\n", df1)
    print()
    print("Second dataframe\n", df2)
    print()
    
    # merge these dataframes, intersection of rows (by index) and unions of columns
    df3 = pd.merge(df1, df2, left_index=True, right_index=True)
    print("Merging two dataframes\n", df3)
    print()
    
    # join these two dataframes, rows from first dataframe and union of columns
    df4 = df1.join(df2)
    print("Joining second dataframe to first\n", df4)
    print()
    
    # concatentate these two dataframes, unions of rows and union of columns
    df5 = pd.concat([df1, df2], axis=1, sort=True)
    print("Concatenating two dataframes\n", df5)

    
run_example()