# Robert Dwan

import logging.handlers
import os
import sys
import timeit
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from FeatureExtraction import extractLexicalFeatures
from VisualizeResults import visualize, evaluateFeatures

algorithms = ["rf", "lr", "svm-l", "svm-rbf"]

handler0 = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "data/log/time-log.log"))
FORMAT0 = '%(message)s'
formatter0 = logging.Formatter(FORMAT0)
handler0.setFormatter(formatter0)
time_log = logging.getLogger()
time_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
time_log.addHandler(handler0)
# Read in csv
dataset = pd.read_csv('data/all_data_labeled.csv')

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values

# Extract some lexical features
features = extractLexicalFeatures(urls)

# Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(labels)

feature_train, feature_test, label_train, label_test = train_test_split(feature, ls, test_size=0.20, random_state=1436)


def machine_learning_algorithm(input_algorithm):
    switcher = {
        "rf": RandomForestClassifier(n_estimators=25, max_depth=None, max_features=0.4, random_state=11),
        "lr": LogisticRegression(multi_class='multinomial', solver='lbfgs'),
        "svm-l": LinearSVC(dual=False, fit_intercept=False, max_iter=1700, C=1),
        "svm-rbf": SVC(kernel='rbf', gamma='auto', max_iter=2000, C=1)
    }
    return switcher.get(input_algorithm, lambda: "Invalid Algorithm")


def __getAlgorithmName(abbreviation):
    algo_dict = {'rf': 'Random Forest', 'lr': 'Logistic Regression', 'svm-l': 'SVM-Linear', 'svm-rbf': 'SVM-rbf'}
    if abbreviation in algo_dict:
        return algo_dict[abbreviation]


def train_and_test(algorithm, feature_selection_algorithm):
    time_log.info('testing time logger')

    start_training_time = timeit.timeit()
    algorithm.fit(feature_train, label_train)
    end_training_time = timeit.timeit()

    start_testing_time = timeit.timeit()
    prediction = algorithm.predict(feature_test)
    end_testing_time = timeit.timeit()

    training_time = end_training_time - start_training_time
    testing_time = end_testing_time - start_testing_time
    logging.info(datetime.now())

    if len(sys.argv) > 1:
        logging.info('Algorithm Run: ' + __getAlgorithmName(sys.argv[1]))
    else:
        logging.info('Algorithm Run: All')
    message = 'Training Time: ' + str(training_time) + 's\n' + 'Testing Time: ' + str(testing_time) + 's\n'
    logging.info(message)

    visualize(label_test, prediction)
    evaluateFeatures(feature_selection_algorithm, feature_train, label_train)


if len(sys.argv) > 1:
    train_and_test(machine_learning_algorithm(sys.argv[1]), sys.argv[1])
else:
    for algo in algorithms:
        train_and_test(machine_learning_algorithm(algo), algo)
