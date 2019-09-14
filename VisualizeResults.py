import logging.handlers
import os
from datetime import datetime
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif, f_classif, chi2
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from FeatureExtraction import FeatureList

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


def visualize(label_test, prediction, eval_algorithm):
    algo = __getAlgorithmName(eval_algorithm)
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
    results_log.info(datetime.now())
    results_log.info('Algorithm Run: ' + algo)
    results_log.info(cmtx.to_string())
    results_log.info(classif_report)
    results_log.info(accuracy)
    generateROC(label_test, prediction, eval_algorithm)
    results_log.info('\n')


def evaluateFeatures(training_features, training_output, labels=None):
    if labels is None:
        new_output = __convertToIntArray(training_output, data_labels)
    else:
        new_output = __convertToIntArray(training_output, labels)
    discriminativeTests(training_features, new_output)
    feature_log.info(datetime.now())
    # TODO: Implement SelectKBest
    # featureVariability(training_features)
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
    featureVar = list()
    for i in range(len(FeatureList)):
        feature_values = data_set[:, i].ravel()
        featureVar.append(np.var(feature_values))
    df = pd.DataFrame(columns=FeatureList)
    df.loc[0] = featureVar
    feature_log.info(df.to_string())
    feature_log.info('\n')


def __getAlgorithmName(abbreviation):
    algo_dict = {'rf': 'Random Forest', 'lr': 'Logistic Regression', 'svm-l': 'SVM-Linear', 'svm-rbf': 'SVM-rbf'}
    if abbreviation in algo_dict:
        return algo_dict[abbreviation]


def generateROC(test, score, eval_algorithm):
    algo = __getAlgorithmName(eval_algorithm)
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    n_classes = len(data_labels)
    roc_auc = dict()
    y_test = label_binarize(test, classes=data_labels)
    y_score = label_binarize(score, classes=data_labels)
    for i in range(n_classes):
        t = y_test[:, i]
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

    # Then interpolate all ROC curves at this points
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(n_classes):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

    # Finally average it and compute AUC
    mean_tpr /= n_classes

    fpr["macro"] = all_fpr
    tpr["macro"] = mean_tpr
    roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

    # Plot all ROC curves
    plt.figure()
    lw = 2
    plt.plot(fpr["micro"], tpr["micro"],
             label='micro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["micro"]),
             color='deeppink', linestyle=':', linewidth=4)

    plt.plot(fpr["macro"], tpr["macro"],
             label='macro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["macro"]),
             color='navy', linestyle=':', linewidth=4)

    colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'skyblue', 'red'])
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                 label='ROC curve for {0} URLs (area = {1:0.2f})'
                       ''.format(data_labels[i], roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=lw)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(algo + ' - Multi-class ROC Curve Plot')
    plt.legend(loc="lower right")
    plt.show()


def __convertToIntArray(training_output, labels):
    new_output = list()
    for url_type in training_output:
        i = labels.index(url_type)
        new_output.append(i)
    return new_output


def discriminativeTests(X, y):
    f_test, p_test = f_classif(X, y)
    chi_score, p_val = chi2(X, y)
    mi = mutual_info_classif(X, y)
    fig, axes = plt.subplots(10, 3, figsize=(9, 9))  # 3 columns each containing 10 figures, total 30 features
    ax = axes.ravel()
    for j in range(len(FeatureList)):
        ax[j].scatter(X[:, j], y, edgecolor='black', s=10)
        ax[j].set_title("{} - F-test={:.2f}, MI={:.2f}, Chi={:.2f}".format(FeatureList[j], f_test[j], mi[j]),
                        chi_score[j], fontsize=8)
    plt.tight_layout()
    plt.show()
