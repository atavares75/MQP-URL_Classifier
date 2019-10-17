import json
import sys
from datetime import datetime as dt

import numpy as np
from DataSet import DataSet
from ModelBuilder.ProbabilityAlgorithmFactory import ProbabilityAlgorithmFactory as af
from OutputGenerator.OutputGenerator import OutputGenerator


def main(json_file):
    """
    This method runs through all the algorithms in the algorithm config file and outputs
    their metrics
    :PARAM json_file: the config file with algorithm, feature_set, and data_set information
    """
    time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    main_path = "/%s-BatchRun" % time

    with open(json_file) as jf:
        batch = json.load(jf)

    i = 0
    for run in batch["runs"]:
        print("HAVE JSON")

        metric = run["metric"]

        path = "%s/Run%s" % (main_path, str(i))

        algorithms = af.get_all_algorithms(run["algorithm"])
        print("HAVE ALGORITHMS")

        training_data_set = DataSet(run["training_set"])
        testing_data_set = DataSet(run["testing_set"])
        print("HAVE DATA")

        training_data_set.set_features(run["feature_set"])
        testing_data_set.set_features(run["feature_set"])
        print("HAVE FEATURES")

        threshold = run["threshold"]

        for algorithm in algorithms:
            print("Running Algorithm " + algorithm.name)
            algorithm.run(training_data_set, testing_data_set)
            output = OutputGenerator(algorithm, testing_data_set, path, metric)
            tags = tag_predictions(threshold, output.model)
            output.print_probability_output(tags)

        i += 1


def tag_predictions(threshold, algorithm):
    """
    Given the threshold and model it creates an array of tags. A tag is given if the class probability is above the threshold.
    :param threshold: float value between 0 and 1
    :param algorithm: the Algorithm class object
    :return: an array of tags. A tag is a string representing a URL category
    """
    predicted_probs = algorithm.performance.prediction
    rows, columns = predicted_probs.shape
    tags = np.zeros(shape=(rows, columns), dtype=object)
    classes = algorithm.algorithm.classes_
    for row in range(rows):
        for column in range(columns):
            if predicted_probs[row][column] >= threshold:
                tags[row][column] = classes[column]
    return tags


main(sys.argv[1])
