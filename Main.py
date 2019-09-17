# Robert Dwan

import json
import sys

import numpy as np
import pandas as pd

from FeatureExtraction.FeatureExtraction import FeatureSet
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from FeatureExtraction.FeatureExtraction import FeatureSet
#from Metrics.	VisualizeResults import visualize, evaluateFeatures, featureVariability

def output_all():
	

def output_wanted():
	

def train_and_test(algorithm, train_feature_set, train_labels, test_feature_set, test_labels):
    print("Training")
    algorithm.fit(train_feature_set, train_labels)
    print("DONE")

	print("Testing")
	prediction = algorithm.predict(test_feature_set)
	print("DONE")
	
	#output_all()
	#ouptut_wanetd()


def main(json_file):
	with open(json_file) as jf:
		run = json.load(jf)
		
	algorithms = af.get_all_algorithms(run["algorithm"])
	train_data = pd.read_csv(run["training_set"])
main(sys.argv[1])
