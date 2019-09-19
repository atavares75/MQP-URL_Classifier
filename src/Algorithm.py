# Robert Dwan

import uuid

from datetime import datetime
from Metrics.VisualizeResults import AlgorithmPerformance

class Algorithm:
	
	def __init__(self, name, parameters, algorithm):
		self.name = name
		self.parameters = parameters
		self.algorithm = algorithm
		self.id = uuid.uuid4()
		
	def run(self, training_set, testing_set):
		start_train = datetime.now()
		self.algorithm.fit(training_set.features, training_set.labels)
		end_train = datetime.now()
		
		self.train_time = end_train - start_train

		start_test = datetime.now()
		self.prediction = self.algorithm.predict(testing_set.features)
		end_test = datetime.now()
		
		self.test_time = end_test - start_test
		
		self.performance = AlgorithmPerformance(testing_set.urls, testing_set.labels, self.prediction, self.name)