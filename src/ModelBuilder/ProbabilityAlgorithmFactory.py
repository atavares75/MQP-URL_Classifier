import json
import sys

from ModelBuilder.ProbabilityAlgorithm import ProbabilityAlgorithm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.semi_supervised import LabelSpreading, LabelPropagation
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


class ProbabilityAlgorithmFactory:

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
            algorithms.append(
                ProbabilityAlgorithmFactory.get_algorithm(algorithm["algorithm"], algorithm["parameters"]))

        return algorithms

    @staticmethod
    def get_algorithm(algorithm_type, parameters):
        """
        :PARAM type: the type of algorithm to be created
        :PARAM parameters: the parameters to pass when creating the algorithm
        :RETURN the created algorithm object
        """
        if algorithm_type == "RandomForest":
            algorithm = ProbabilityAlgorithm(algorithm_type, parameters, RandomForestClassifier(**parameters))
        elif algorithm_type == "LogisticRegression":
            algorithm = ProbabilityAlgorithm(algorithm_type, parameters, LogisticRegression(**parameters))
        elif algorithm_type == "SVM-L":
            algorithm = ProbabilityAlgorithm(algorithm_type, parameters, LinearSVC(**parameters))
        elif algorithm_type == "SVM-RBF":
            algorithm = ProbabilityAlgorithm(algorithm_type, parameters, SVC(**parameters))
        elif algorithm_type == 'Spreading':
            algorithm = ProbabilityAlgorithm(algorithm_type, parameters, LabelSpreading(**parameters))
        elif algorithm_type == 'Propagation':
            algorithm = ProbabilityAlgorithm(algorithm_type, parameters, LabelPropagation(**parameters))
        else:
            print("Error: Invalid algorithm")
            sys.exit()

        return algorithm
