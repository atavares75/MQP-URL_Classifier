import json
import sys
import numpy as np
from DataSet import DataSet
from ModelBuilder.ProbabilityAlgorithmFactory import ProbabilityAlgorithmFactory as af
from OutputGenerator import OutputGenerator


def main(json_file):
    """
    This method runs through all the algorithms in the algorithm config file and outputs
    their metrics
    :PARAM json_file: the config file with algorithm, feature_set, and data_set information
    """
    with open(json_file) as jf:
        batch = json.load(jf)

    for run in batch["runs"]:
        print("HAVE JSON")

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
            output = OutputGenerator(algorithm, testing_data_set)
            tags = tag_predictions(threshold, output.model)
            output.print_probability_output(tags)

def tag_predictions(threshold, model):
    predicted_probs = model.performance.prediction
    rows, columns = predicted_probs.shape
    tags = np.zeros(shape=(rows, columns), dtype=object)
    classes = model.algorithm.classes_
    for row in range(rows):
        for column in range(columns):
            if predicted_probs[row][column] >= threshold:
                tags[row][column] = classes[column]
    return tags



main(sys.argv[1])
