"""
Some examples of numerical computations on numpy arrays

https://scipy-lectures.org/intro/numpy/operations.html
"""

import numpy as np

SIZE = 10

# create some 1D numpy array and some slices
np_ints = np.linspace(-SIZE, SIZE - 1, 2 * SIZE)
print(np_ints)
np_evens = np_ints[0::2]
np_odds = np_ints[1::2]
print(np_evens)
print(np_odds)


# Operations on single array - reductions
print(np.sum(np_evens))
print(np.min(np_odds))


# Operations on arrays of same shape
print(np_evens * np_odds)
print(np_odds > np_evens)


# Operations on arrays of diffent shapes
print(np_evens ** np.array(2))
print(np_evens ** np.full(np_evens.shape, 2))     # manually broadcast

# vectorization - creat new vector operations
my_abs = lambda x: x if x > 0 else -x
vec_abs = np.vectorize(my_abs)
print(vec_abs(np_odds))









