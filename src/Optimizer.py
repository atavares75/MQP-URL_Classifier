import copy
import json
import sys
from datetime import datetime as dt

from DataSet import DataSet
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from OutputGenerator.OutputGenerator import OutputGenerator


def main(json_file):
    """
    This method runs an algorithm several times while changing the tuning_param
    This will output metrics for all run and identify the value for the tuning_param
    with the highest accuracy.
    :PARAM json_file: the config file containing the algorithm and the values to use
    """
    time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = "/%s-OptimizedRun" % time

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
    tuning_params = run["tuning_param"]
    parameters = run["parameters"]
    mins = run["min"]
    maxs = run["max"]
    steps = run["step"]
    metric = run["metric"]

    if (len(tuning_params) == 2):
        i = mins[0]
        while i <= maxs[0]:
            j = mins[1]
            while j <= maxs[1]:
                temp_params = copy.deepcopy(parameters)
                temp_params.update({tuning_params[0]: i, tuning_params[1]: j})
                algorithm = af.get_algorithm(name, temp_params)

                if i == mins[0] and j == mins[1]:
                    best = [algorithm, [i, j]]

                algorithm.run(training_data_set, testing_data_set)

                output = OutputGenerator(algorithm, testing_data_set, path, metric)
                output.print_2d_optimized_output(tuning_params, i, j)

                if metric == "accuracy":
                    if algorithm.performance.get_results(metric) > best[0].performance.get_results(metric):
                        best = [algorithm, [i, j]]
                elif algorithm.performance.get_results(metric).values.mean() < best[0].performance.get_results(
                        metric).values.mean():
                    best = [algorithm, [i, j]]

                j += steps[1]

            i += steps[0]

        output.print_optimized_parameters(best)
    else:
        i = mins
        while i <= maxs:
            temp_params = copy.deepcopy(parameters)
            temp_params.update({tuning_params: i})
            algorithm = af.get_algorithm(name, temp_params)

            if i == mins:
                best = [algorithm, i]

            algorithm.run(training_data_set, testing_data_set)

            output = OutputGenerator(algorithm, testing_data_set, path, metric)
            output.print_1d_optimized_output(i)

            if metric == "accuracy":
                if algorithm.performance.get_results(metric) > best[0].performance.get_results(metric):
                    best = [algorithm, i]
            elif algorithm.performance.get_results(metric).values.mean() < best[0].performance.get_results(
                    metric).values.mean():
                best = [algorithm, i]

            i += steps
        output.print_optimized_parameters(best)


main(sys.argv[1])
