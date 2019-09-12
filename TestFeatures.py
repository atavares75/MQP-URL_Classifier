import logging.handlers
import os

import numpy as np
import pandas as pd

from FeatureExtraction import extractLexicalFeatures
from VisualizeResults import evaluateFeatures

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
dataset = pd.read_csv('data/all_data_labeled.csv')

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values

# Extract some lexical features
features = extractLexicalFeatures(urls)
# Convert to numpy arrays
feature = np.asarray(features.to_numpy())
ls = np.asarray(labels)

# var = featureVariability(feature)
evaluateFeatures(feature, ls)
