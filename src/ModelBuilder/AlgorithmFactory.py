# Robert Dwan

import json, sys

from src.Algorithm import Algorithm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


class AlgorithmFactory:

    @staticmethod
    def get_algorithm(algorithm_type, parameters):
        """
        :PARAM type: the type of algorithm to be created
        :PARAM parameters: the parameters to pass when creating the algorithm
        :RETURN the created algorithm object
        """
        if algorithm_type == "RandomForest":
            algorithm = Algorithm(algorithm_type, parameters, RandomForestClassifier(**parameters))
        elif algorithm_type == "LogisticRegression":
            algorithm = Algorithm(algorithm_type, parameters, LogisticRegression(**parameters))
        elif algorithm_type == "SVM-L":
            algorithm = Algorithm(algorithm_type, parameters, LinearSVC(**parameters))
        elif algorithm_type == "SVM-RBF":
            algorithm = Algorithm(algorithm_type, parameters, SVC(**parameters))
        else:
            print("Error: Invalid algorithm")
            sys.exit()

        return algorithm

    @staticmethod
    def get_all_algorithms(json_file):
        """
        :PARAM json_file: the file containing the configuration for one or more algorithms
        :RETURN a list of all the algorithms specified in the config file
        """
        with open(json_file) as jf:
            all_runs = json.load(jf)

        algorithms = []
        algorithm_names = []

        for algorithm in all_runs["algorithms"]:
            algorithms.append(AlgorithmFactory.get_algorithm(algorithm["algorithm"], algorithm["parameters"]))

        return algorithms
