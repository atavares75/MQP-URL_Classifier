# Robert Dwan

import json
import sys
from datetime import datetime as dt

from DataSet import DataSet
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
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

        for algorithm in algorithms:
            print("Running Algorithm " + algorithm.name)
            algorithm.run(training_data_set, testing_data_set)
            output = OutputGenerator(algorithm, testing_data_set, path, metric)
            output.print_algorithm_performance()

        i += 1

main(sys.argv[1])
