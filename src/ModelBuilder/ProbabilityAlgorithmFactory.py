import json
import sys

from ModelBuilder.ProbabilityAlgorithm import ProbabilityAlgorithm as Algorithm
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, BaggingClassifier, GradientBoostingClassifier, \
    AdaBoostClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
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
            algorithm = Algorithm(algorithm_type, parameters, RandomForestClassifier(**parameters))
        elif algorithm_type == "LogisticRegression":
            algorithm = Algorithm(algorithm_type, parameters, LogisticRegression(**parameters))
        elif algorithm_type == 'Spreading':
            algorithm = Algorithm(algorithm_type, parameters, LabelSpreading(**parameters))
        elif algorithm_type == 'Propagation':
            algorithm = Algorithm(algorithm_type, parameters, LabelPropagation(**parameters))
        elif algorithm_type == 'ExtraTrees':
            algorithm = Algorithm(algorithm_type, parameters, ExtraTreesClassifier(**parameters))
        elif algorithm_type == 'AdaBoost':
            if "base_estimator" in parameters:
                estimator_path = parameters["base_estimator"]
                algorithm = ProbabilityAlgorithmFactory.get_all_algorithms(estimator_path)[0]
                parameters["base_estimator"] = algorithm.algorithm
            algorithm = Algorithm(algorithm_type, parameters, AdaBoostClassifier(**parameters))

        elif algorithm_type == 'Gradient':
            algorithm = Algorithm(algorithm_type, parameters, GradientBoostingClassifier(**parameters))

        elif algorithm_type == 'Bagging':
            if "base_estimator" in parameters:
                estimator_path = parameters["base_estimator"]
                algorithm = ProbabilityAlgorithmFactory.get_all_algorithms(estimator_path)[0]
                parameters["base_estimator"] = algorithm.algorithm
            algorithm = Algorithm(algorithm_type, parameters, BaggingClassifier(**parameters))

        elif algorithm_type == 'MLP':
            algorithm = Algorithm(algorithm_type, parameters, MLPClassifier(**parameters))
        else:
            print("Error: Invalid algorithm")
            sys.exit()

        return algorithm
