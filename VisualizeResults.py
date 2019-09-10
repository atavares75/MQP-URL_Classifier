import logging.handlers
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from FeatureExtraction import extractLexicalFeatures

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "data/log/results-log.log"))
FORMAT = '%(message)s'
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
results_log = logging.getLogger('data/log/results-log.log')
results_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
results_log.addHandler(handler)

handler2 = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "data/log/feature-log.log"))
FORMAT2 = '%(message)s'
formatter2 = logging.Formatter(FORMAT2)
handler2.setFormatter(formatter2)
feature_log = logging.getLogger("data/log/feature-log.log")
feature_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
feature_log.addHandler(handler2)

data_labels = ['Normal', 'malware', 'phish', 'ransomware', 'BotnetC&C']

FeatureList = ['Length of URL',
               'Number of ‘.’ In URL',
               'Number of ‘@‘ in URL',
               'Params in URL',
               'Queries in URL',
               'Fragments in URL',
               'Entropy of Domain name',
               'Check for Non Standard port',
               'Domain name in Alexa Top 1 Million',
               'Check for non-ascii characters',
               'Check for popular domains in subdomains',
               '’-‘ in domain name',
               'Digits in domain name',
               'Length of host',
               'Number of ‘.’ in domain name',
               'IP based host name',
               'Hex based host name',
               'Check for common TLD',
               'Length of path',
               'Count ‘-‘ in path',
               'Count ‘/‘ in path',
               'Count ‘=‘ in path',
               'Count ‘;‘ in path',
               'Count ‘,‘ in path',
               'Count ‘_‘ in path',
               'Count ‘.’ in path',
               'Count ‘?’ in path',
               'Count ‘&’ in path',
               'Username and Password in path']


def visualize(label_test, prediction):
    c_matrix = confusion_matrix(label_test, prediction, data_labels)
    cmtx = pd.DataFrame(
        c_matrix,
        index=['true:' + data_labels[0], 'true:' + data_labels[1], 'true:' + data_labels[2], 'true:' + data_labels[3],
               'true:' + data_labels[4]],
        columns=['pred:' + data_labels[0], 'pred:' + data_labels[1], 'pred:' + data_labels[2], 'pred:' + data_labels[3],
                 'pred:' + data_labels[4]]
    )
    classif_report = classification_report(label_test, prediction)
    accuracy = accuracy_score(label_test, prediction)
    results_log.info(cmtx.to_string())
    results_log.info(classif_report)
    results_log.info(accuracy)
    results_log.info('\n')


def evaluateFeatures(eval_algorithm, training_features, training_output):
    algo = evaluation_algorithm(eval_algorithm)
    selector = RFECV(algo, step=1, cv=5)
    selector = selector.fit(training_features, training_output)
    e = selector.support_
    f = selector.score(training_features, training_output)
    feature_log.info(e)
    feature_log.info(f)
    feature_log.info('\n')


def evaluation_algorithm(input_algorithm):
    switcher = {
        "rf": RandomForestClassifier(n_estimators=25, max_depth=None, random_state=11),
        "lr": LogisticRegression(multi_class='multinomial', solver='lbfgs'),
        "svm-l": LinearSVC(dual=False, fit_intercept=False, max_iter=1700, C=1),
        "svm-rbf": SVC(kernel='rbf', gamma='auto', max_iter=10000, C=1)
    }
    return switcher.get(input_algorithm, lambda: "Invalid Algorithm")


def displayFeatureHistogram(data_set, target):
    data_set['target'] = target
    fig, axes = plt.subplots(10, 3, figsize=(12, 9))  # 3 columns each containing 10 figures, total 30 features
    normal = data_set.loc[data_set['target'] == data_labels[0]]
    malware = data_set.loc[data_set['target'] == data_labels[1]]
    phish = data_set.loc[data_set['target'] == data_labels[2]]
    ransomware = data_set.loc[data_set['target'] == data_labels[3]]
    botnet = data_set.loc[data_set['target'] == data_labels[4]]
    data_set.drop('target', 1, inplace=True)
    normal.drop('target', 1, inplace=True)
    malware.drop('target', 1, inplace=True)
    phish.drop('target', 1, inplace=True)
    ransomware.drop('target', 1, inplace=True)
    botnet.drop('target', 1, inplace=True)
    ax = axes.ravel()  # flat axes with numpy ravel
    for i in range(29):
        _, bins = np.histogram(data_set.to_numpy(), bins=10)
        ax[i].hist(normal.to_numpy()[:, i], bins=bins, color='green', alpha=.5)
        ax[i].hist(malware.to_numpy()[:, i], bins=bins, color='red', alpha=0.3)
        ax[i].hist(phish.to_numpy()[:, i], bins=bins, color='yellow', alpha=0.3)
        ax[i].hist(ransomware.to_numpy()[:, i], bins=bins, color='skyblue', alpha=0.3)
        ax[i].hist(botnet.to_numpy()[:, i], bins=bins, color='black', alpha=0.3)
        ax[i].set_title(FeatureList[i], fontsize=9)
        ax[i].axes.get_xaxis().set_visible(False)
        ax[i].set_yticks(())
    ax[0].legend(data_labels, loc='best', fontsize=8)
    plt.tight_layout()
    plt.show()


def featureVariability(data_set):
    featureVar = np.var(data_set.to_numpy())
    feature_log.info(featureVar)


dataset = pd.read_csv('data/all_data_labeled.csv')

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values

# Extract some lexical features
features = extractLexicalFeatures(urls)
# displayFeatureHistogram(features, labels)
featureVariability(features)
