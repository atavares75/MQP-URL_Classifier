from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif, f_classif, chi2
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import label_binarize


class AlgorithmPerformance:

    def __init__(self, test_urls, test_output, prediction, algorithm=""):
        """
        Initializes parameters to generate algorithm performance metrics
        :param test_urls: the labeled input the model was tested with 
        :param test_output: the labeled output model was tested with
        :param prediction: the predicted output of model
        :param algorithm: algorithm used by model (default is empty string)
        """
        self.data_labels = np.unique(test_output)
        self.test_urls = test_urls
        self.test_output = test_output
        self.prediction = prediction
        self.algorithm = algorithm

    def createConfusionMatrix(self):
        """
        Creates a confusion matrix from the predicted and actual output
        :return: a data frame with the confusion matrix and labelled rows and column
        """
        c_matrix = confusion_matrix(self.test_output, self.prediction, self.data_labels)
        idx = list()
        c = list()
        for label in self.data_labels:
            idx.append('true: ' + label)
            c.append('pred: ' + label)
        cmtx = pd.DataFrame(c_matrix, index=idx, columns=c)
        return cmtx

    def createClassificationReport(self):
        """
        Creates a classification report
        :return: returns a dictionary containing classification report
        """
        return classification_report(self.test_output, self.prediction)

    def calculateAccuracy(self):
        """
        Returns the accuracy of the prediction
        :return: float
        """
        return accuracy_score(self.test_output, self.prediction)

    def generateROC(self):
        """
        Generates an ROC curve and ROC area for each class
        :return: plot with ROC curve
        """
        fpr = dict()
        tpr = dict()
        n_classes = len(self.data_labels)
        roc_auc = dict()
        y_test = label_binarize(self.test_output, classes=self.data_labels)
        y_score = label_binarize(self.prediction, classes=self.data_labels)
        for i in range(n_classes):
            t = y_test[:, i]
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

        all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

        mean_tpr = np.zeros_like(all_fpr)
        for i in range(n_classes):
            mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

        mean_tpr /= n_classes

        fpr["macro"] = all_fpr
        tpr["macro"] = mean_tpr
        roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

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
        plt.title(self.algorithm + ' - Multi-class ROC Curve Plot')
        plt.legend(loc="lower right")
        return plt.gcf()


class FeaturePerformance:

    def __init__(self, features, labeled_output):
        """
        Initialized parameters needed to evaluate features
        :param features: FeatureSet
        :param labeled_output: labeled output of feature set
        """
        self.features = features
        self.labeled_output = labeled_output

    def calculateF_Value(self):
        """
        Calculates ANOVA F-value for the features
        :return: tuple of the set of f-values and a set of p-values
        """
        f_test, p_test = f_classif(self.features, self.labeled_output)
        return f_test, p_test

    def calculateChiX_Score(self):
        """
        Computes chi-squared stats between each non-negative feature and class.
        :return: tuple containing chi2 statistics of each feature and p-values of each feature
        """
        chi_score, p_val = chi2(self.features, self.labeled_output)
        return chi_score, p_val

    def calculateMutualInformation(self):
        """
        Estimates mutual information for a discrete target variable
        :return: Estimated mutual information between each feature and the target
        """
        mi = mutual_info_classif(self.features, self.labeled_output)
        return mi

    def generateFeaturePlots(self, f_test, mutual_info, chi_score):
        """
        Creates a plot for each of the features in the feature set with their f-value, estimated mutual information,
        and chi-squared statistic
        :param f_test: f-values
        :param mutual_info: estimated mutual information between each feature and the target
        :param chi_score: chi-squared statistic for each feature
        :return: a plt containing subplots fot each feature
        """
        fig, axes = plt.subplots(10, 3, figsize=(9, 9))  # 3 columns each containing 10 figures, total 30 features
        ax = axes.ravel()
        for j in range(len(self.features.FeatureList)):
            ax[j].scatter(self.features[:, j], self.labeled_output, edgecolor='black', s=10)
            ax[j].set_title("{:s} F-test={:.2f}, MI={:.2f}, Chi={:.2f}".format(self.features.FeatureList[j], f_test[j],
                                                                               mutual_info[j]), chi_score[j],
                            fontsize=8)
        plt.tight_layout()
        return plt.gcf()

    def buildCorrelationHeatMap(self):
        """
        Creates a heat map of the correlations between all the features
        :return: a plot containing the heat map
        """
        correlation = self.features.df.corr(method='kendall')
        ax = sns.heatmap(correlation, xticklabels=True, yticklabels=True, vmin=0, vmax=1, linewidths=.2, cmap="YlGnBu",
                         square=True)
        return plt.gcf()
