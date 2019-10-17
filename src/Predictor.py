import json
import os
import sys
from datetime import datetime as dt

import joblib
import pandas as pd
from DataSet import DataSet
from ModelBuilder.Algorithm import Algorithm
from OutputGenerator.OutputGenerator import output_path


def main(json_file):
    """
    Takes an exisiting models and a data set and makes predictions on the data
    :PARAM json_file: config file with model, feature_set, and data set
    """
    time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = output_path + "/%s-PredictionRun" % time
    os.mkdir(path)

    with open(json_file) as jf:
        get_model = json.load(jf)

    model = Algorithm(get_model["name"], [], joblib.load(get_model["model"]))
    testing_data_set = DataSet(get_model["testing_set"])
    testing_data_set.set_features(get_model["feature_set"])

    prediction = model.algorithm.predict(testing_data_set.features)

    df = pd.DataFrame()
    df['prediction'] = prediction
    df['url'] = pd.DataFrame(testing_data_set.urls)
    df.to_csv("%s/prediction.csv" % path)


main(sys.argv[1])
