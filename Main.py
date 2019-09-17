# Robert Dwan

import json
import sys

import numpy as np
import pandas as pd

from FeatureExtraction.FeatureExtraction import FeatureSet
from Metrics.VisualizeResults import AlgorithmPerformance
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from datetime import datetime


class TrainTest:

    def __init__(self, algorithm, train_feature_set, train_labels, test_feature_set):
        self.algorithm = algorithm
        print("Training")
        start_train = datetime.now()
        self.algorithm.fit(train_feature_set, train_labels)
        end_train = datetime.now()
        print("DONE")
        self.train_time = end_train - start_train

        print("Testing")
        start_test = datetime.now()
        self.prediction = self.algorithm.predict(test_feature_set)
        end_test = datetime.now()
        print("DONE")
        self.test_time = end_test - start_test


def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    algorithms, algorithm_names = af.get_all_algorithms(run["algorithm"])
    train_data = pd.read_csv(run["training_set"])
    test_data = pd.read_csv(run["testing_set"])
    train_labels = train_data['label']
    train_urls = train_data['url']
    test_labels = test_data['label']
    test_urls = test_data['url']
    train_feature_set = np.asarray(FeatureSet(run["feature_set"], train_urls).df)
    test_feature_set = np.asarray(FeatureSet(run["feature_set"], test_urls).df)

    for algorithm, name in zip(algorithms, algorithm_names):
        tt = TrainTest(algorithm, train_feature_set, train_labels, test_feature_set)
        ap = AlgorithmPerformance(test_labels, tt.prediction, name)


main(sys.argv[1])
