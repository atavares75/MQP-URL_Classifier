import logging.handlers
import os
import sys

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from FeatureExtraction import extractLexicalFeatures, FeatureList
from IsolatedDatasetGenerator import convertData
from VisualizeResults import evaluateFeatures, data_labels

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
dataset = pd.read_csv('data/full_5050_training_set.csv')

argsGood = True

# makes sure types aren't repeated
selections = list()

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        if arg not in data_labels or arg in selections:
            argsGood = False
        else:
            selections.append(arg)

if 2 < len(sys.argv) < 6 and argsGood:
    urlData = dataset.loc[dataset['label'] == sys.argv[1]]
    i = 2
    for arg in sys.argv[2:]:
        temp = dataset.loc[dataset['label'] == sys.argv[i]]
        urlData = pd.concat([urlData, temp], ignore_index=True, sort=False)
        i = i + 1
else:
    urlData = dataset

# Store URLs and their labels
urls = urlData.iloc[:, 3].values
labels = urlData.iloc[:, 2].values

# Extract some lexical features
features = extractLexicalFeatures(urls)
# Convert to numpy arrays
feature = np.asarray(features.to_numpy())
ls = np.asarray(labels)

new_label = None
if len(sys.argv) == 2:
    if sys.argv[1] in data_labels:
        new_label = ['Other', sys.argv[1]]
        ls = convertData(sys.argv[1], ls)

evaluateFeatures(feature, ls, new_label)

data = pd.DataFrame(feature, columns=FeatureList)
corl = data.corr(method='kendall')
ax = sns.heatmap(corl, xticklabels=True, yticklabels=True, vmin=0, vmax=1, linewidths=.2, cmap="YlGnBu", square=True)
plt.show()
