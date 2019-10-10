import uuid
from datetime import datetime

from Metrics.AlgorithmPerformance import AlgorithmPerformance


class Algorithm:

    def __init__(self, name, parameters, algorithm):
        """
        Initialize variables for an algorithm
        :PARAM name: the name of the algorithm
        :PARAM parameters: the parameters for the algorithm
        :PARAM algorithm: the algorithm object
        """
        self.name = name
        self.parameters = parameters
        self.algorithm = algorithm
        self.id = uuid.uuid4()

    def run(self, training_set, testing_set):
        """
        This method runs the algorithm by train and testing it and get the performance object
        :PARAM training_set: the data set the algorithm trains on
        :PARAM testing_set: the data set the algorithm tests on
        """
        start_train = datetime.now()
        self.algorithm.fit(training_set.features, training_set.labels)
        end_train = datetime.now()

        self.train_time = end_train - start_train

        start_test = datetime.now()
        self.prediction = self.algorithm.predict(testing_set.features)
        end_test = datetime.now()

        self.test_time = end_test - start_test

        self.performance = AlgorithmPerformance(testing_set.urls, testing_set.labels, self.prediction, self.name)


    def runSpecial(self, train_features, train_labels, testing_features, testing_labels, urls):
        """
        This method runs the algorithm by train and testing it and get the performance object
        :param train_features: array of features
        :param train_labels: array of labels
        :param testing_features: array of features
        :param testing_labels: array of labels
        :param urls: array of urls
        :return:
        """
        start_train = datetime.now()
        self.algorithm.fit(train_features, train_labels)
        end_train = datetime.now()

        self.train_time = end_train - start_train

        start_test = datetime.now()
        self.prediction = self.algorithm.predict(testing_features)
        end_test = datetime.now()

        self.test_time = end_test - start_test

        self.performance = AlgorithmPerformance(urls, testing_labels, self.prediction, self.name)
