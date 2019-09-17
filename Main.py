# Robert Dwan

import json
import sys

import numpy as np
import pandas as pd

from FeatureExtraction.FeatureExtraction import FeatureSet
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af


# from Metrics/VisualizeResults import visualize, evaluateFeatures, featureVariability

def train_and_test(algorithm, train_feature_set, train_labels, test_feature_set, test_labels):
    print("Training")
    algorithm.fit(train_feature_set, train_labels)
    print("DONE")

    print("Testing")
    prediction = algorithm.predict(test_feature_set)
    print("DONE")


def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    algorithms = af.get_all_algorithms(run["algorithm"])
    train_data = pd.read_csv(run["training_set"])
    test_data = pd.read_csv(run["testing_set"])
    train_labels = train_data['label']
    train_urls = train_data['url']
    test_labels = test_data['label']
    test_urls = test_data['url']
    train_feature_set = np.asarray(FeatureSet(run["feature_set"], train_urls).df)
    test_feature_set = np.asarray(FeatureSet(run["feature_set"], test_urls).df)

    for algorithm in algorithms:
        train_and_test(algorithm, train_feature_set, train_labels, test_feature_set, test_labels)


main(sys.argv[1])
