# Robert Dwan

import pandas as pd
import numpy as np

from FeatureExtraction.FeatureExtraction import FeatureSet

class DataSet:

	def __init__(self, csv_file):
		"""
		Initialize the varaibles for the data set
		:PARAM csv_file: the csv file containging the data
		"""
		self.data = pd.read_csv(csv_file)
		self.labels = self.data['label']
		self.urls = self.data['url']
		
	def set_features(self, json_file):
		"""
		Thid method sets the feature array for the data set
		:PARAM json_file: the config file for what features to use
		"""
		self.features = np.asarray(FeatureSet(json_file, self.urls).df)