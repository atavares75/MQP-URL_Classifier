# Robert Dwan 

import json, sys

from ModelBuilder.Algorithm import Algorithm
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, BaggingClassifier, \
    VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.semi_supervised import LabelSpreading, LabelPropagation


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
        elif algorithm_type == 'Spreading':
            algorithm = Algorithm(algorithm_type, parameters, LabelSpreading(**parameters))
        elif algorithm_type == 'Propagation':
            algorithm = Algorithm(algorithm_type, parameters, LabelPropagation(**parameters))

        elif algorithm_type == 'AdaBoost':
            if "base_estimator" in parameters:
                estimator_path = parameters["base_estimator"]
                algorithm = AlgorithmFactory.get_all_algorithms(estimator_path)[0]
                parameters["base_estimator"] = algorithm.algorithm
            algorithm = Algorithm(algorithm_type, parameters, AdaBoostClassifier(**parameters))

        elif algorithm_type == 'Gradient':
            algorithm = Algorithm(algorithm_type, parameters, GradientBoostingClassifier(**parameters))

        elif algorithm_type == 'Bagging':
            if "base_estimator" in parameters:
                estimator_path = parameters["base_estimator"]
                algorithm = AlgorithmFactory.get_all_algorithms(estimator_path)[0]
                parameters["base_estimator"] = algorithm.algorithm
            algorithm = Algorithm(algorithm_type, parameters, BaggingClassifier(**parameters))

        elif algorithm_type == 'Voting':
            if "estimators" in parameters:
                estimator_path = parameters["estimators"]
                algorithms = AlgorithmFactory.get_all_algorithms(estimator_path)
                estimators = list()
                for algorithm in algorithms:
                    estimators.append((algorithm.name, algorithm.algorithm))
                parameters["estimators"] = estimators
            algorithm = Algorithm(algorithm_type, parameters, VotingClassifier(**parameters))
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

        for algorithm in all_runs["algorithms"]:
            algorithms.append(AlgorithmFactory.get_algorithm(algorithm["algorithm"], algorithm["parameters"]))

        return algorithms

    @staticmethod
    def get_probability_algorithm(algorithm_type, parameters):
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
