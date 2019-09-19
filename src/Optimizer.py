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
	testing_data_set.set_features(run["feature_set"])
	print("HAVE FEATURES")	
		
	name = run["algorithm"]
	tuning_param = run["tuning_param"]
	parameters = run["parameters"]
	min = run["min"]
	max = run["max"]
	step = run["step"]
	
	i = self.min
	while i <= self.max:
		temp_params = paramters.append({self.tuning_param, i})
		algorithm = af.get_algorithm(self.name, temp_params)
		
		if i == min:
			best = [algorithm, min]
		
		algorithm.run(training_data_set, testing_data_set)
		output = OutputGenerator(algorithm, testing_data_set)
		output.print_all()
		if algorithm.performance.getAccuracy() > best[0].performance.getAccuracy():
			best = [algorithm, i]
			
		print(best)
		i += step

main(sys.argv[1])
