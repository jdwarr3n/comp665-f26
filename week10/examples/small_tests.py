"""
Practice for week 10 of Data Visualization

Tests input for closest pairs functions derive from Coursera class
"""

# The first 11 test inputs were derived by hand

# The remaining test inputs were derived by analyzing large tests cases that failed during hierarchical clustering
# and derived a small test that detected the same error

# The trailing comments indicates errors being caught


TEST_DATA = [[[0, 0], [1, 0]],			# base case
            [[1.1, 0], [1, 0.8]],		# base case
            [[0, 0], [0, 1], [0, 2]],	        # base case
            [[0, 0], [1, 1], [3, 2]],	        # base case
            [[0, 0], [1, 1], [2, 2]],	        # base case
            [[row, col] for row in range(4) for col in range(1)], 	# uniform vertical line
            [[row, col] for row in range(1) for col in range(4)], 	# unifomr horizontal line
            [[row, col] for row in range(2) for col in range(2)], 	# grid
            [[row, col] for row in range(-1, 2) for col in range(-1, 2)], 	# grid
            [[1.0, 0.0], [5.0, 0.0], [4.0, 0.0], [7.0, 0.0]],            
            [[1.0, 1.0], [1.0, 5.0], [1.0, 4.0], [1.0, 7.0]],            # sort in x, but unsorted in y
             
            [[0.7, 0.24], [0.1, 0.42], [0.33, 0.39], [0.21, 0.51]],      # always returns default tuple
            [[0.02, 1.0], [0.02, 0.74], [0.1, 0.11], [0.44, 0.12], [0.61, 0.7]],   # failed to compute inverse indices
            [[0.5, 0.2], [0.09, 0.07], [0.72, 0.08], [0.97, 0.09], [0.07, 0.29], [0.88, 0.94]],  # strip is everything
            [[0.11, 0.75], [0.62, 0.86], [0.65, 0.68], [0.68, 0.48], [0.7, 0.9], [0.79, 0.18]],  # additional test based on student failures
            [[0.38, 0.26], [0.42, 0.03], [0.48, 0.23], [0.8, 0.65], [0.95, 0.85], [0.97, 0.61]], # additional test based on student failures
            [[0.61, 0.8], [0.54, 0.8], [0.76, 0.94], [0.39, 0.4], [0.32, 0.16]],   # strip is too wide
            [[0.23, 0.94], [0.91, 0.6], [0.65, 0.08], [0.94, 0.9], [0.66, 0.43]],  # strip is too narrow
            [[0.53, 0.24], [0.95, 0.85], [0.6, 0.42], [0.57, 0.32], [0.37, 0.28]], # strip is empty
            [[0.66, 0.63], [0.7, 0.68], [0.78, 0.63], [0.1, 0.9], [0.9, 0.05]],    # failed to iterate over last element in outer loop
            [[0.87, 0.63], [0.37, 0.81], [0.7, 0.59], [0.73, 0.9], [0.1, 0.16]],   # failed to iterate over last element in inner loop
            [[0.74, 0.9], [0.03, 0.69], [0.76, 0.92], [0.16, 0.09], [0.13, 0.34]], # cluster_list in place strip
            [[-4.0, 0.0], [0.0, -1.0], [0.0, 1.0], [4.0, 0.0]],                    # closest pair in strip are three apart
            [[-1.0, 0.0], [-0.99, -10.0], [-0.98, -20.0], [0.98, 20.0], [0.99, 10.0], [1.0, 0.0]], # catches failure to sort strip
            [[-4.0, 0.0], [-2.0, 0.0], [0.0, -0.1], [0.0, 0.1], [2.0, 0.0], [4.0, 0.0]],    #failure to extract distance from divide part
            [[0.89, 0.28], [0.34, 0.57], [0.26, 0.92], [0.35, 0.15], [0.05, 0.11], [0.6, 0.41]], # strip_center = (left_list[-1].horiz_center() + right_list[1].horiz_center()) / 2.0
            [[0.68, 0.48], [0.65, 0.68], [0.7, 0.9], [0.11, 0.75], [0.62, 0.86], [0.79, 0.18]],  # NEW - for idx2 in range(idx1 + 1, min(4, len(strip))):
            [[0.38, 0.26], [0.48, 0.23], [0.42, 0.03], [0.95, 0.85], [0.8, 0.65], [0.97, 0.61]], # NEW - improper split in fast_closest_pairs, first one short
            [[0.02, 0.39], [0.19, 0.75], [0.35, 0.03], [0.73, 0.81], [0.76, 0.88], [0.78, 0.11]]] # NEW - improper split in fast_closest_pairs

##for pts in TEST_DATA:
##    new_pts = pts[:]
##    new_pts.sort(key = lambda pt: pt[0])
##    if pts != new_pts:
##        print(pts, "has unsorted x-corodinates")