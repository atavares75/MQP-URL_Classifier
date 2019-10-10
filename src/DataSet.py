import numpy as np
import pandas as pd
from FeatureExtraction.FeatureExtraction import FeatureSet
from sklearn.feature_selection import f_classif, chi2, mutual_info_classif, SelectKBest


class DataSet:

    def __init__(self, csv_file=None, urls=None):
        """
        Initialize the variables for the data set
        :PARAM csv_file: the csv file containing the data
        :param urls: pandas DataFrame containing urls
        """
        if csv_file is not None:
            self.data = pd.read_csv(csv_file, dtype={"label": object, "url": object})
        else:
            self.data = urls
        self.labels = self.data['label']
        self.urls = self.data['url']

    def set_features(self, json_file):
        """
        This method sets the feature array for the data set
        :PARAM json_file: the config file for what features to use
        """
        self.features = np.asarray(FeatureSet(json_file, self.urls).df)

    def set_KBest_features(self, k, score_func):
        axis = {
            "Chi-Squared": chi2,
            "F-Test": f_classif
        }
        kbest_features = SelectKBest(axis[score_func], k).fit(self.features, np.asarray(self.labels))
        self.kbest = kbest_features.transform(self.features)

    def rank_features(self, k, score_func):
        axis = {
            "Chi-Squared": chi2,
            "F-Test": f_classif
        }
        self.ranked_features = SelectKBest(axis[score_func], k).fit(self.features, np.asarray(self.labels)).scores_

