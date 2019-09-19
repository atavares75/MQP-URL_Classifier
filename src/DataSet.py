# Robert Dwan

import pandas as pd
import numpy as np

from FeatureExtraction.FeatureExtraction import FeatureSet

class DataSet:

	def __init__(self, csv_file):
		self.data = pd.read_csv(csv_file)
		self.labels = self.data['label']
		self.urls = self.data['url']
		
	def set_features(self, json_file):
		self.features = FeatureSet(json_file, self.urls).df.to_numpy()