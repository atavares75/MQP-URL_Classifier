# Robert Dwan

import logging.handlers
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from FeatureExtraction import extractLexicalFeatures
from VisualizeResults import visualize, evaluateFeatures, featureVariability

algorithms = ["rf", "lr", "svm-l", "svm-rbf"]

handler0 = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "data/log/time-log.log"))
FORMAT0 = '%(message)s'
formatter0 = logging.Formatter(FORMAT0)
handler0.setFormatter(formatter0)
time_log = logging.getLogger('data/log/time-log.log')
time_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
time_log.addHandler(handler0)
# Read in csv
training = pd.read_csv('data/8020_training_set.csv')
test = pd.read_csv('data/labeled_test_set.csv')

# Store URLs and their labels
urls = training.iloc[:, 3].values
labels = training.iloc[:, 2].values

test_urls = test.iloc[:, 2].values
test_labels = test.iloc[:, 1].values

# Extract some lexical features
features = extractLexicalFeatures(urls)
test_features = extractLexicalFeatures(test_urls)

# Convert to numpy arrays
feature = np.asarray(features.to_numpy())
ls = np.asarray(labels)
test_feature = np.asarray(test_features.to_numpy())

feature_train = feature
label_train = ls
feature_test = test_feature
label_test = test_labels

def machine_learning_algorithm(input_algorithm):
    switcher = {
        "rf": RandomForestClassifier(n_estimators=25, max_depth=None, max_features=0.4, random_state=11),
        "lr": LogisticRegression(multi_class='multinomial', solver='lbfgs'),
        "svm-l": LinearSVC(dual=False, fit_intercept=False, max_iter=1700, C=1),
        "svm-rbf": SVC(kernel='rbf', gamma='auto', max_iter=10000, C=1)
    }
    return switcher.get(input_algorithm, lambda: "Invalid Algorithm")


def __getAlgorithmName(abbreviation):
    algo_dict = {'rf': 'Random Forest', 'lr': 'Logistic Regression', 'svm-l': 'SVM-Linear', 'svm-rbf': 'SVM-rbf'}
    if abbreviation in algo_dict:
        return algo_dict[abbreviation]

def print_false_positives(correct, prediction, label):
    print("Normal False Positives")
    for i in range (len(correct)):
        if correct[i] != label:
            if prediction[i] == label:
                print(correct[i] + ": " + test_urls[i])
		
def train_and_test(algorithm, feature_selection_algorithm):
    time_log.info('testing time logger')
    print("Started Training")
    start_training_time = datetime.now()
    algorithm.fit(feature_train, label_train)
    end_training_time = datetime.now()
    print("Stopped Training")
    print("Started Testing")
    start_testing_time = datetime.now()
    prediction = algorithm.predict(feature_test)
    end_testing_time = datetime.now()
    print("Stopped Testing")
    training_time = end_training_time - start_training_time
    testing_time = end_testing_time - start_testing_time
    time_log.info(datetime.now())

    time_log.info('Algorithm Run: ' + __getAlgorithmName(feature_selection_algorithm))

    message = 'Training Time: ' + str(training_time) + '\n' + 'Testing Time: ' + str(testing_time) + '\n'
    time_log.info(message)

    visualize(label_test, prediction, feature_selection_algorithm)
    #evaluateFeatures(feature_selection_algorithm, feature_train, label_train)
	
    print_false_positives(label_test, prediction, "Normal")

if len(sys.argv) > 1:
    train_and_test(machine_learning_algorithm(sys.argv[1]), sys.argv[1])
else:
    for algo in algorithms:
        train_and_test(machine_learning_algorithm(algo), algo)
