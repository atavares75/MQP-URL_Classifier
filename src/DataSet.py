import numpy as np
import pandas as pd
from FeatureExtraction.FeatureExtraction import FeatureSet


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
        Thid method sets the feature array for the data set
        :PARAM json_file: the config file for what features to use
        """
        self.features = np.asarray(FeatureSet(json_file, self.urls).df)
