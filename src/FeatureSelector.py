import copy
import json
import sys
from datetime import datetime as dt

import numpy as np
from DataSet import DataSet
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from OutputGenerator.OutputGenerator import OutputGenerator
from pandas import DataFrame


def main(json_file):
    """
    This method runs an algorithm several times while changing the tuning_param
    This will output metrics for all run and identify the value for the tuning_param
    with the highest accuracy.
    :PARAM json_file: the config file containing the algorithm and the values to use
    """
    time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = "/%s-FeatureOptimizedRun" % time

    with open(json_file) as jf:
        run = json.load(jf)

    training_data_set = DataSet(run["training_set"])
    testing_data_set = DataSet(run["testing_set"])
    print("HAVE DATA")
    training_data_set.set_features(run["feature_set"])
    print("HALFWAY")
    testing_data_set.set_features(run["feature_set"])
    print("HAVE FEATURES")

    name = run["algorithm"]
    parameters = run["parameters"]
    min = run["min_features"]
    max = run["max_features"]
    steps = run["step"]
    score_func = run["score_function"]
    metric = run["metric"]



    i = min
    index = 0
    length = int((max - min) / steps + 1)
    arr = np.zeros(shape=(length, 2))
    training_data_set.rank_features(max, score_func)
    while i <= max:
        temp_params = copy.deepcopy(parameters)
        algorithm = af.get_algorithm(name, temp_params)

        training_data_set.set_KBest_features(i, score_func)
        testing_data_set.set_KBest_features(i, score_func)

        if i == min:
            best = [algorithm, i]

        algorithm.runSpecial(training_data_set.kbest, training_data_set.labels, testing_data_set.kbest, testing_data_set.labels, testing_data_set.urls)

        output = OutputGenerator(algorithm, testing_data_set, path, metric)
        output.print_optimized_feature_output(i)

        if metric == "accuracy":
            if algorithm.performance.get_results(metric) > best[0].performance.get_results(metric):
                best = [algorithm, i]
            arr[index] = [i, algorithm.performance.get_results(metric)]
        else:
            if algorithm.performance.get_results(metric).values.mean() < best[0].performance.get_results(
                    metric).values.mean():
                best = [algorithm, i]
            arr[index] = [i, algorithm.performance.get_results(metric).values.mean()]
        index += 1
        i += steps

    axis = {
        "accuracy": "Accuracy (%)",
        "false_positive": "False Positive Rate (%)",
        "false_negative": "False Negative Rate (%)"
    }
    rf = DataFrame(data=training_data_set.ranked_features)
    df = DataFrame(arr, columns=["k", axis[metric]])
    output.print_feature_optimization_visual(df, rf)


main(sys.argv[1])
