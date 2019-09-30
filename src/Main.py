# Robert Dwan

import json
import os
import sys
from datetime import datetime as dt

from DataSet import DataSet
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from OutputGenerator import OutputGenerator


def main(json_file):
    """
    This method runs through all the algorithms in the algorithm config file and outputs
    their metrics
    :PARAM json_file: the config file with algorithm, feature_set, and data_set information
    """
    time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    main_path = "../../outputs/%s-BatchRun" % time
    os.mkdir(main_path)
	
    with open(json_file) as jf:
        batch = json.load(jf)	
		
    i = 0
    for run in batch["runs"]:
        print("HAVE JSON")
		
        metric = run["metric"]
		
        path = "%s/Run%s" % (main_path, str(i))
        os.mkdir(path)
        file = open("%s/%s.txt" % (path, metric), "w")
		
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
            output = OutputGenerator(algorithm, testing_data_set, path)
            output.print_all()
            file.write("Algorithm name: " + algorithm.name)
            file.write("\nParameter values are: " + str(algorithm.parameters))
            file.write("\nRun ID: " + str(algorithm.id) + "\n")
            file.write(metric + ":\n" + str(algorithm.performance.get_results(metric)))
            file.write("\n\n")
			
        file.close()
        i += 1

main(sys.argv[1])
