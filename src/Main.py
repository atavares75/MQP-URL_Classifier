# Robert Dwan

import json, sys

from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from DataSet import DataSet
from OutputGenerator import OutputGenerator

def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    algorithms = af.get_all_algorithms(run["algorithm"])
    training_data_set = DataSet(run["training_set"])
    testing_data_set = DataSet(run["testing_set"])
    training_data_set.set_features(run["feature_set"])
    testing_data_set.set_features(run["feature_set"])

    for algorithm in algorithms:
        algorithm.run(training_data_set, testing_data_set)
        output = OutputGenerator(algorithm, testing_data_set)
        output.print_all()

main(sys.argv[1])
