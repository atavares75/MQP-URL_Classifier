# Robert Dwan

import joblib
import json
import sys
from DataSet import DataSet
from ModelBuilder.Algorithm import Algorithm
from OutputGenerator.OutputGenerator import OutputGenerator


def main(json_file):
    with open(json_file) as jf:
        get_model = json.load(jf)

    model = Algorithm(get_model["name"], [], joblib.load(get_model["model"]))
    training_data_set = DataSet(get_model["training_set"])
    testing_data_set = DataSet(get_model["testing_set"])

    training_data_set.set_features(get_model["feature_set"])
    testing_data_set.set_features(get_model["feature_set"])

    model.run(training_data_set, testing_data_set)

    output = OutputGenerator(model, testing_data_set)
    output.print_all()


main(sys.argv[1])
