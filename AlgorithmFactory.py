# Robert Dwan

import sys
import json

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

class AlgorithmFactory:

	@staticmethod
	def get_algorithm(type, parameters):
	"""
	:PARAM type: the type of algorithm to be created
	:PARAM parameters: the parameters to pass when creating the algorithm
	:RETURN the created algorithm object
	"""
		if type == "RandomForest":
			algorithm = RandomForestClassifier(**parameters)
		elif type == "LogisticRegression":
			algorithm = LogisticRegression(**parameters)
		elif type == "SVM-L":
			algorithm = LinearSVC(**parameters)
		elif type == "SVM-RBF":
			algorithm = SVC(**parameters)
		else:
			print("Error: Invalid algorithm")
			sys.exit() 
			
		return algorithm
		
	@staticmethod
	def get_all_algorithms(json_file):
	"""
	:PARAM json_file: the file containing the configuration for one or more algorithms
	:RETURN a list of all the algorithms specfied in the config file
	"""
		with open(json_file) as jf:
			all_runs = json.load(jf)
			
		algorithms = []	
			
		for algorithm in all_runs["algorithms"]:
			algorithms.append(AlgorithmFactory.get_algorithm(algorithm["algorithm"], algorithm["parameters"]))
			
		return algorithms