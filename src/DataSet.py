# Robert Dwan

import pandas as pd
import numpy as np

from FeatureExtraction.FeatureExtraction import FeatureSet

class DataSet:

	def __init__(self, csv_file=None, urls=None):
		if csv_file is not None:
			self.data = pd.read_csv(csv_file, dtype={"label": object, "url": object})
		else:
			self.data = urls
		self.labels = self.data['label']
		self.urls = self.data['url']
		
	def set_features(self, json_file):
		self.features = np.asarray(FeatureSet(json_file, self.urls).df)

	def set_data(self, data):
		self.data = data