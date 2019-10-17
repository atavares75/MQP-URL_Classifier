import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import f_classif, chi2


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
        Calculates ANOVA F-value for the features.
        Wrapper for scikit learn f_classif function.
        :return: tuple of the set of f-values and a set of p-values
        """
        f_test, p_test = f_classif(self.features.df.to_numpy(), self.labeled_output)
        return f_test, p_test

    def calculateChiX_Score(self):
        """
        Computes chi-squared stats between each non-negative feature and class.
        Wrapper for scikit learn chi2 function.
        :return: tuple containing chi2 statistics of each feature and p-values of each feature
        """
        chi_score, p_val = chi2(self.features.df.to_numpy(), self.labeled_output)
        return chi_score, p_val

    def buildCorrelationHeatMap(self):
        """
        Creates a heat map of the correlations between all the features.
        :return: a plot containing the heat map
        """
        correlation = self.features.df.corr(method='kendall')
        sns.heatmap(correlation, xticklabels=True, yticklabels=True, vmin=0, vmax=1, linewidths=.2, cmap="YlGnBu",
                    square=True)
        return plt.gcf()
