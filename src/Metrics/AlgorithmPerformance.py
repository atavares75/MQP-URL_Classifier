from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import label_binarize


class AlgorithmPerformance:

    def __init__(self, test_urls, test_output, prediction, algorithm, autoGenerateMetrics=True):
        """
        Initializes parameters to generate algorithm performance metrics
        :param test_urls: the labeled input the model was tested with
        :param test_output: the labeled output model was tested with
        :param prediction: the predicted output of model
        :param algorithm: algorithm used by model (default is empty string)
        :param autoGenerateMetrics: boolean value indicating if all metrics should be automatically generated
        """
        self.data_labels = np.unique(test_output)
        self.test_urls = test_urls
        self.test_output = test_output
        self.prediction = prediction
        self.algorithm = algorithm
        if autoGenerateMetrics is True:
            self.cmtx = self.createConfusionMatrix()

            self.FP = self.cmtx.sum(axis=0) - np.diag(self.cmtx)
            self.FN = self.cmtx.sum(axis=1) - np.diag(self.cmtx)
            self.TP = np.diag(self.cmtx)
            self.TN = self.cmtx.values.sum() - (self.FP.values.sum() + self.FN.values.sum() + self.TP.sum())
        else:
            self.cmtx = None

            self.FP = None
            self.FN = None
            self.TP = None
            self.TN = None

    def createConfusionMatrix(self):
        """
        Creates a confusion matrix from the predicted and actual output
        :return: a data frame with the confusion matrix and labeled rows and column
        """
        c_matrix = confusion_matrix(self.test_output, self.prediction, self.data_labels)
        idx = list()
        c = list()
        for label in self.data_labels:
            idx.append('true: ' + label)
            c.append('pred: ' + label)
        self.cmtx = pd.DataFrame(c_matrix, index=idx, columns=c)
        self.FP = self.cmtx.sum(axis=0) - np.diag(self.cmtx)
        self.FN = self.cmtx.sum(axis=1) - np.diag(self.cmtx)
        self.TP = np.diag(self.cmtx)
        self.TN = self.cmtx.values.sum() - (self.FP.values.sum() + self.FN.values.sum() + self.TP.sum())
        return self.cmtx

    def createClassificationReport(self):
        """
        Wrapper function for sklearn.metrics classification_report function
        :return: returns a dictionary containing classification report
        """
        return classification_report(self.test_output, self.prediction)

    def calculateAccuracy(self):
        """
        Wrapper function for sklearn.metrics accuracy_score function
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

    def calculateFalsePostiveRate(self):
        """
        :RETURN: returns the false positive rate
        """
        return self.FP / (self.FP + self.TN)

    def calculateFalseNegativeRate(self):
        """
        :RETURN: returns the false negative rate
        """
        return self.FN / (self.TP + self.FN)

    def get_results(self, metric):
        """
        This method returns the wanted metric inputted by the user
        :PARAM metric: the wanted metric inputed by the user
        :RETURN: the value of the wanted metric
        """
        if metric == "accuracy":
            return self.calculateAccuracy()
        elif metric == "false_positive":
            return self.calculateFalsePostiveRate()
        elif metric == "false_negative":
            return self.calculateFalseNegativeRate()

    def set_prediction(self, new):
        self.prediction = pd.Series(new)
