import logging.handlers
import os

import numpy as np
import pandas as pd
from IsolatedDatasetGenerator import convertData

from FeatureExtraction import extractLexicalFeatures

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
training = pd.read_csv('data/5050_training_set.csv')
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

convertData('phish', label_train, label_test)

