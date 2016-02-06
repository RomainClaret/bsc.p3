# -*- coding: utf-8 -*-

import numpy
from scipy.cluster.vq import kmeans, vq
import scipy.spatial.distance

__author__ = "Romain Claret"
__maintainer__ = "Romain Claret"
__copyright__ = "Copyright 2016, Romain Claret "
__credits__ = ["Romain Claret"]

# Copyright (C) Romain Claret, All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
__license__ = "Proprietary and confidential"
__version__ = "1.0.0"
__email__ = "romain.claret@rocla.ch"
__status__ = "Prototype"  # Prototype, Development, Production
__date__ = "19.01.2016"


"""@package kmeans_nD
Documentation for the K-Means algorithm in the context of this application.

This K-means works in N Dimensions. It is possible to also get the cosine distance
from a vector to the clusters.
"""


def get_clusters_centroids(data, number_of_clusters):
    """
    Calculate the positions of the centroids of the clusters.
    This algorithm will try to respect the number of clusters asked, however
    the result amount may be less.
    :param data: Multi directional matrix of meanings
    :param number_of_clusters: maximum amount of clusters
    :return: the list of clusters centroids
    """
    # convert list into vstack
    data = numpy.vstack(data)

    # computing K-Means
    centroids, distortion = kmeans(data, number_of_clusters)

    return centroids.tolist()


def get_index_assign_data_to_cluster(data, list_of_clusters):
    """
    Gives the cluster that the multi direction vectors matches
    :param data: Multi directional matrix of meanings
    :param list_of_clusters: List of clusters centroids
    :return: the list of the cluster number in the order of the data
    """
    # assign each sample to a cluster
    index, distortion = vq(data, list_of_clusters)

    return index


def cos_cdist_clusters(clusters, vector):
    """
    Compute the cosine distances between each row of cluster matrix and vector.
    :param clusters: List of clusters centroids
    :param vector: vector to get the distance from
    :return: list of cosine distances for the clusters and a vector
    """
    matrix = numpy.array(clusters)
    vector = numpy.array(vector)
    v = vector.reshape(1, -1)
    return scipy.spatial.distance.cdist(matrix, v, 'cosine').reshape(-1)


if __name__ == "__main__":
    """
    This function is run if this file is run directly.

    It will get the list of centroids and the cosine distance for dummies values.
    """

    number_of_clusters = 3
    data_sample = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 3.5], [7, 2.5], [8, 1.5], [0, 0]]
    classify_me = [1.5, 1.5]

    list_of_clusters = get_clusters_centroids(data_sample, number_of_clusters)
    print("List of centroids for the clusters: " + str(list_of_clusters))
    print("List of cosine distance with classify_me: " +str(list(cos_cdist_clusters(list_of_clusters, classify_me))))
