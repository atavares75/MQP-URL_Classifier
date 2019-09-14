from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, f_classif, chi2
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import label_binarize


class Evaluate:
    classif_report = None
    accuracy = None
    cmtx = None
    ROC = None
    discriminativeFeaturePlots = None

    def __init__(self, training_set, algorithm, training_output):
        self.features = training_set
        self.eval_algorithm = algorithm
        self.labeled_output = training_output
        self.data_labels = np.unique(training_output)

    def visualize(self, label_test, prediction, eval_algorithm):
        c_matrix = confusion_matrix(label_test, prediction, self.data_labels)
        idx = list()
        c = list()
        for label in self.data_labels:
            idx.append('true:' + label)
            c.append('pred:' + label)
        self.cmtx = pd.DataFrame(c_matrix, index=idx, columns=c)
        self.classif_report = classification_report(label_test, prediction)
        self.accuracy = accuracy_score(label_test, prediction)
        self.generateROC(label_test, prediction, eval_algorithm)

    def evaluateFeatures(self, training_features, training_output, labels=None):
        if labels is None:
            new_output = self.__convertToIntArray(training_output, self.data_labels)
        else:
            new_output = self.__convertToIntArray(training_output, labels)
        self.discriminativeTests(training_features, new_output)
        # TODO: Implement SelectKBest

    def __getAlgorithmName(self, abbreviation):
        algo_dict = {'rf': 'Random Forest', 'lr': 'Logistic Regression', 'svm-l': 'SVM-Linear', 'svm-rbf': 'SVM-rbf'}
        if abbreviation in algo_dict:
            return algo_dict[abbreviation]

    def generateROC(self, test, score, eval_algorithm):
        # Compute ROC curve and ROC area for each class
        fpr = dict()
        tpr = dict()
        n_classes = len(self.data_labels)
        roc_auc = dict()
        y_test = label_binarize(test, classes=self.data_labels)
        y_score = label_binarize(score, classes=self.data_labels)
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
                           ''.format(self.data_labels[i], roc_auc[i]))

        plt.plot([0, 1], [0, 1], 'k--', lw=lw)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(eval_algorithm + ' - Multi-class ROC Curve Plot')
        plt.legend(loc="lower right")
        self.ROC = plt.gcf()

    def __convertToIntArray(self, training_output, labels):
        new_output = list()
        for url_type in training_output:
            i = labels.index(url_type)
            new_output.append(i)
        return new_output

    def discriminativeTests(self, X, y):
        f_test, p_test = f_classif(X, y)
        chi_score, p_val = chi2(X, y)
        mi = mutual_info_classif(X, y)
        fig, axes = plt.subplots(10, 3, figsize=(9, 9))  # 3 columns each containing 10 figures, total 30 features
        ax = axes.ravel()
        for j in range(len(self.features.FeatureList)):
            ax[j].scatter(X[:, j], y, edgecolor='black', s=10)
            ax[j].set_title(
                "{} - F-test={:.2f}, MI={:.2f}, Chi={:.2f}".format(self.features.FeatureList[j], f_test[j], mi[j]),
                chi_score[j], fontsize=8)
        plt.tight_layout()
        self.discriminativeFeaturePlots = plt.gcf()
