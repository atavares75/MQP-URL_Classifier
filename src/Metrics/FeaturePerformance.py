import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import mutual_info_classif, f_classif, chi2


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
        f_test, p_test = f_classif(self.features.df.to_numpy(), self.labeled_output)
        return f_test, p_test

    def calculateChiX_Score(self):
        """
        Computes chi-squared stats between each non-negative feature and class.
        :return: tuple containing chi2 statistics of each feature and p-values of each feature
        """
        chi_score, p_val = chi2(self.features.df.to_numpy(), self.labeled_output)
        return chi_score, p_val

    def calculateMutualInformation(self):
        """
        Estimates mutual information for a discrete target variable
        :return: Estimated mutual information between each feature and the target
        """
        mi = mutual_info_classif(self.features.df.to_numpy(), self.labeled_output)
        return mi

    # def generateFeaturePlots(self, f_test, mutual_info, chi_score):
    #     """
    #     Creates a plot for each of the features in the feature set with their f-value, estimated mutual information,
    #     and chi-squared statistic
    #     :param f_test: f-values
    #     :param mutual_info: estimated mutual information between each feature and the target
    #     :param chi_score: chi-squared statistic for each feature
    #     :return: a plt containing subplots fot each feature
    #     """
    #     f = f_test.flatten()
    #     m = mutual_info.flatten()
    #     c = chi_score.flatten()
    #     fig, axes = plt.subplots(10, 3, figsize=(9, 9))  # 3 columns each containing 10 figures, total 30 features
    #     ax = axes.ravel()
    #     for j in range(len(self.features.FeatureList)):
    #         ax[j].scatter(self.features.df.iloc[:, j], self.labeled_output, edgecolor='black', s=10)
    #         ax[j].set_title("{:s} F-test={:.2f}, MI={:.2f}, Chi={:.2f}".format(self.features.FeatureList[j], f[j],
    #                                                                            m[j], c[j], fontsize=8))
    #     plt.tight_layout()
    #     return plt.gcf()

    def buildCorrelationHeatMap(self):
        """
        Creates a heat map of the correlations between all the features
        :return: a plot containing the heat map
        """
        correlation = self.features.df.corr(method='kendall')
        sns.heatmap(correlation, xticklabels=True, yticklabels=True, vmin=0, vmax=1, linewidths=.2, cmap="YlGnBu",
                    square=True)
        return plt.gcf()
