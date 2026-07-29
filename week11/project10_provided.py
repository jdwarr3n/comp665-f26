"""
Provided code for projects 10 and 11

Includes definition of Cluster class and plotting code
"""

import random
import math
import pandas as pd
import matplotlib.pyplot as plt


# Location of cancer risk data in csv files of various sizes
DATA_PATH = "data/"
PLOTS_PATH = "../docs/week11/plots/"
DATA_24 = DATA_PATH + "cancer_risk_24.csv"
DATA_111 = DATA_PATH + "cancer_risk_111.csv"
DATA_290 = DATA_PATH + "cancer_risk_290.csv"
DATA_896 = DATA_PATH + "cancer_risk_896.csv"
DATA_3108 = DATA_PATH + "cancer_risk_3108.csv"
MAP = DATA_PATH + "USA_Counties_1000x634.png"

# Class definition for clusters used in hierarchical and k-means clustering algorithms
class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "provided".
        """
        rep = "provided.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, risk_frame):
        """
        Input: dataframe risk_frame containing risks used in creating singleton clusters
        
        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        codes = self.fips_codes()
        for fips in codes:
            singleton_cluster = Cluster(set([fips]),
                                        risk_frame.loc[fips, X_CENTER],
                                        risk_frame.loc[fips, Y_CENTER],
                                        risk_frame.loc[fips, POP],
                                        risk_frame.loc[fips, RISK])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error
            



###########################################################################
# Helper functions for reading dataframe and forming lists of singleton clusters

# Headers for dataframe
FIPS, X_CENTER, Y_CENTER, POP, RISK = "FIPS", "x center", "y center","population", "cancer risk"
COL_TYPES = {FIPS : "str", X_CENTER : "float", Y_CENTER : "float", POP : "int", RISK : "float"}

def risk_csv_to_dataframe(risk_file):
    """
    Input: string risk_file
    Output: dataframe that contains cancer risk data in risk_file
    """
    
    frame = pd.read_csv(risk_file,
                        header=None,
                        usecols=[0, 1, 2, 3, 4],
                        names=[FIPS, X_CENTER, Y_CENTER, POP, RISK],
                        dtype=COL_TYPES)
    frame.set_index(FIPS, inplace=True)
    return frame


def dataframe_to_singleton_clusters(risk_frame):
    """
    Input: pandas dataframe risk_frame with cancer risk data
    Output: List of clusters corresponding to each county in risk_frame
    """
    
    singletons = []
    for fips, row in risk_frame.iterrows():
        singleton = Cluster(set([fips]), row[X_CENTER], row[Y_CENTER], row[POP], row[RISK])
        singletons.append(singleton)
    
    return singletons



############################################################################################
# Code for plotting clusters

# Define constants for plots
PIXELS_PER_INCH = 80
SIZE_CONSTANT = math.pi / (200.0 ** 2)

# Helper functions
def marker_size(population):
    """
    Input: integer population
    
    Output: Area of circle in pixels proportional to population for use in plt.scatter
    """
    return  SIZE_CONSTANT * population


def plot_image(img_name, title="USA counties"):
    """
    Input: string img_name, optional string title
    
    Output: matplotlib figure of the specified USA map including the 
    specified title and specified size in inches as determined by PIXELS_PER_INCH
    """
    
    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    with open(img_name, 'rb') as img_file:        # using 'r' causes Python to crash :(
        img = plt.imread(img_file)
    
    #  Get dimensions of image and size plot proportional to size of PNG image
    y_pixels, x_pixels, dummy = img.shape
    fig, axs = plt.subplots(figsize=(x_pixels / PIXELS_PER_INCH, 
                                     y_pixels / PIXELS_PER_INCH))
    axs.set_title(title)
    axs.imshow(img)
    return fig


# Main cluster plotting function

# Define colors for clusters.  Display a max of 16 clusters.
COLORS = ['Aqua', 'Yellow', 'Blue', 'Fuchsia', 'Black', 'Green', 'Lime', 'Maroon', 'Navy', 'Olive', 'Orange', 'Purple', 'Red', 'Brown', 'Teal']

def plot_clusters_members(cluster_list, risk_frame, title="Clusters of counties with high cancer risk", save_plot=False):
    """
    Input: List cluster_list, dataframe risk_frame (indexed by FIPS),
    string title, boolean save_plot
    
    Output: matplotlib figure with plot of USA map with cluster members distinguished by color
    """

    fig = plot_image(MAP, title)
    axs = fig.axes[0]

    # draw the counties colored by cluster on the map
    for cluster_idx in range(len(cluster_list)):
        cluster = cluster_list[cluster_idx]
        cluster_color = COLORS[cluster_idx % len(COLORS)]
        x_centers = []
        y_centers = []
        sizes = []
        for fips_code in cluster.fips_codes():
            x_centers.append(risk_frame.loc[fips_code, X_CENTER])
            y_centers.append(risk_frame.loc[fips_code, Y_CENTER])
            sizes.append(marker_size(risk_frame.loc[fips_code, POP]))          
        axs.scatter(x=x_centers, y=y_centers, s=sizes, c=cluster_color)
    
    if save_plot:
        fig.savefig(PLOTS_PATH + title + ".png")
    return fig



        
    
    
            
