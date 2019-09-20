# Robert Dwan

import json, sys

from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from DataSet import DataSet
from OutputGenerator import OutputGenerator

def main(json_file):
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
	tuning_param = run["tuning_param"]
	parameters = run["parameters"]
	min = run["min"]
	max = run["max"]
	step = run["step"]
	
	i = min
	while i <= max:
		temp_params = parameters
		temp_params.update({tuning_param: i})
		algorithm = af.get_algorithm(name, temp_params)
		
		if i == min:
			best = [algorithm, min]
		
		algorithm.run(training_data_set, testing_data_set)
		output = OutputGenerator(algorithm, testing_data_set)
		output.print_all()
		if algorithm.performance.calculateAccuracy() > best[0].performance.calculateAccuracy():
			best = [algorithm, i]
			
		i += step
		
	print(best[0].id + best[1])

main(sys.argv[1])
