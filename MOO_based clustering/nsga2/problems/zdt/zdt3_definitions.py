from __future__ import division
import math, os
import numpy as np
import itertools

from sklearn.metrics import *
from scipy.spatial import distance
from nsga2 import seq
from nsga2.problems.problem_definitions import ProblemDefinitions



class ZDT3Definitions(ProblemDefinitions):

    def __init__(self, individual_list,individual_id_list,individual_ref_id_list):
        self.individual_list = individual_list
        self.individual_id_list = individual_id_list
        self.individual_ref_id_list = individual_ref_id_list

    
    """
    Compute Fuzzy Partition Coefficient as f1
    """
    def f1(self, individual):
        return individual.fpc
    """
    Compute PBM Score of each choromosome as f2
    """
    def f2(self, individual):
        individual_features = individual.features
        individual_length= int(len(individual_features)/individual.no_of_Cluster)
        centers = [individual_features[i:(i + individual_length)] for i in range(0, len(individual_features), individual_length)]
        distance_list = []
        for a, b in itertools.combinations(centers, 2):
            d1 = distance.euclidean(a, b)
            distance_list.append(d1)
        Dc = max(distance_list)
        Ec = np.sum(individual.partition_matrix * individual.distance_matrix)
        PBM_index = math.pow((Dc / (individual.no_of_Cluster * Ec)), 2)
        return PBM_index



    """
        Compute DB-index as f3
    """
    def f3(self, individual):
        all_data_columnmatrix = np.vstack(self.individual_list)
        DB = davies_bouldin_score(all_data_columnmatrix, individual.labels)
        return DB
