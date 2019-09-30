import json

import pandas as pd
from FeatureExtraction import functionSwitcher
from FeatureExtraction.Extractor import Extractor
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder


class FeatureSet:
    """
    Class that constructs and contains feature data frame
    """

    def __init__(self, config_path, url_list):
        """
        Initialized parameters needed for the rest of the functions
        :param config_path: path to feature extraction configuration file
        :param url_list: list of urls as strings
        """
        with open(config_path) as fe:
            selectedFeatures = json.load(fe)
        self.FeatureList = list()
        for feature in selectedFeatures["FeatureList"]:
            self.FeatureList.append(feature["Feature"])
        self.df = self.__extractFeatures(url_list)

    def __extractFeatures(self, url_list):
        """
        From the list of features defined in config file it generates feature set
        :param url_list: list of URLs as strings
        :return: A panda DataFrame containing features of each URL
        """
        features = list()
        i = 0
        for url in url_list:
            i = i + 1
            data_point = list()
            if type(url) is str:
                ex = Extractor(url)
                for feature in self.FeatureList:
                    fun = functionSwitcher(ex, feature)
                    if fun is None:
                        continue
                    else:
                        method, params = fun
                    if params is None:
                        result = method()
                    else:
                        result = method(**params)
                    data_point.append(result)
            else:
                print(i)
                print(str(url))
            features.append(data_point)
        df = DataFrame(features, columns=self.FeatureList)
        obj_df = df.select_dtypes(include=['object']).copy()
        other_df = df.select_dtypes(exclude=['object']).copy()
        encoder = LabelEncoder()
        if not obj_df.empty:
            encoded_columns = encoder.fit_transform(obj_df).reshape(obj_df.to_numpy().shape)
            encoded_df = DataFrame(encoded_columns, columns=obj_df.columns)
        else:
            encoded_df = obj_df
        new_df = pd.concat([other_df, encoded_df], axis=1)
        return new_df
