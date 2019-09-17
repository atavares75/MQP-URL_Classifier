# Robert Dwan

import json
import sys, os

import numpy as np
import pandas as pd
import uuid
import joblib

from FeatureExtraction.FeatureExtraction import FeatureSet
from Metrics.VisualizeResults import AlgorithmPerformance
from ModelBuilder.AlgorithmFactory import AlgorithmFactory as af
from datetime import datetime


class TrainTest:

    def __init__(self, algorithm, train_feature_set, train_labels, test_feature_set):
        self.algorithm = algorithm
        
        start_train = datetime.now()
        self.algorithm.fit(train_feature_set, train_labels)
        end_train = datetime.now()

        self.train_time = end_train - start_train

        start_test = datetime.now()
        self.prediction = self.algorithm.predict(test_feature_set)
        end_test = datetime.now()

        self.test_time = end_test - start_test
        print("DONE TESTING")


class OutputGenerator:

    def __init__(self, trainTest, algorithmPerformance):
        self.id = uuid.uuid4()
        self.trainTest = trainTest
        self.ap = algorithmPerformance
		
    def print_all(self):
        path = "outputs/%s_%s_Output" % (self.id, self.ap.algorithm)
        os.mkdir(path)
		
        file = open("%s/metric_report.txt" % path, "w")
		
        file.write("Output for: " + self.ap.algorithm + "\n")
        file.write("\nTime to train: ")
        file.write(str(self.trainTest.train_time))
        file.write("\nTime to test: ")
        file.write(str(self.trainTest.test_time))
        file.write("\n\nConfusion Matrix:\n")
        file.write(self.ap.createConfusionMatrix().to_string())
        file.write("\n\nClassification Report:\n")
        file.write(self.ap.createClassificationReport())
        file.write("\n\nAccuracy: " + str(self.ap.calculateAccuracy()))
		
        file.close()
		
        fig = self.ap.generateROC()
        fig.savefig('%s/ROC_Graph.png' % path, bbox_inches = 'tight')
		
        joblib.dump(self.trainTest.algorithm, '%s/model.joblib' % path)
		
def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    print("HAVE JSON")
    algorithms, algorithm_names = af.get_all_algorithms(run["algorithm"])
    print("HAVE ALGORITHMS")
    train_data = pd.read_csv(run["training_set"])
    test_data = pd.read_csv(run["testing_set"])
    train_labels = train_data['label']
    train_urls = train_data['url']
    test_labels = test_data['label']
    test_urls = test_data['url']
    train_feature_set = np.asarray(FeatureSet(run["feature_set"], train_urls).df)
    test_feature_set = np.asarray(FeatureSet(run["feature_set"], test_urls).df)

    print("HELLO")
    for algorithm, name in zip(algorithms, algorithm_names):
        tt = TrainTest(algorithm, train_feature_set, train_labels, test_feature_set)
        ap = AlgorithmPerformance(test_labels, tt.prediction, name)
        output = OutputGenerator(tt, ap)
        output.print_all()

main(sys.argv[1])
