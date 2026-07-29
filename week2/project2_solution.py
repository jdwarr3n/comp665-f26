#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Solution for week 2 practice in Data Visualization

Compute binomial distribution and plot its histogram using matplotlib
"""

import random
import matplotlib.pyplot as plt


# In[2]:


# Resource paths
DATA_PATH = "data/"


# In[3]:


###################################################################
# Student code for computing binomial distribution (machine-graded)

def compute_distribution(flips, trials, seed=None):
    """
    Input: Integers flips, trials, optional integer seed
    
    Output: List of integers of length trials, generated via fliping a coin flips times
    
    NOTE: seed is used to initialize the random number generate for deterministic testing
    """ 
    
    if seed:
        random.seed(seed)
        
    distribution = []
    for dummy_trial in range(trials):
        heads = 0
        for dummy in range(flips):
            if random.randrange(2) == 0:
                heads += 1
        distribution.append(heads)
    
    return distribution


# In[5]:


###########################################################
# Student code for plotting distribution in matplotlib - (peer-graded)

def plot_distribution(distribution, num_bins, title="Binomial distribution"):
    """
    Input: List distribution of integers, integer num_bins, optional string title
    
    Output: matplotlib figure containing histogram of distribution with specified 
    number of bins and provided title
    """
    fig = plt.figure()
    bin_boundaries = [-0.5 + idx for idx in range(num_bins + 1)]
    plt.hist(distribution, bin_boundaries)
    plt.title(title)
    plt.xlabel("Number of heads")
    plt.ylabel("Number of trials")
    return fig

