import json
import os
import sys
import uuid
from datetime import datetime as dt
import pandas as pd
from FeatureExtraction.FeatureExtraction import FeatureSet
from Metrics.FeaturePerformance import FeaturePerformance
from OutputGenerator.OutputGenerator import output_path
from pandas import DataFrame


class FeatureEvaluation:

    def __init__(self, feature_set_config_path, urls, labels, metric, path):
        fs = FeatureSet(feature_set_config_path, urls)

        fp = FeaturePerformance(fs, labels)

        if metric == "Correlation":
            heat_map = fp.buildCorrelationHeatMap()
            heat_map.savefig('%s/%s-HeatMap.png' % (metric, path), bbox_inches='tight')
            return

        file = open("%s/features_eval_%s.csv" % (path, metric), "w")

        if metric == "Chi-Squared":
            score, p_val = fp.calculateChiX_Score()
            score_name = "Chi-Score"
        if metric == "F-Test":
            score, p_val = fp.calculateF_Value()
            score_name = "F-Value"

        df = DataFrame(columns=fs.FeatureList, index=[score_name, 'P-Value'])
        df.iloc[0] = score
        df.iloc[1] = p_val

        df.to_csv(file)

        file.close()


def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = output_path + "/%s-FeatureEvaluation" % time
    if not os.path.exists(path):
        os.mkdir(path)


    i = 0
    for feature in run["feature_set"]:
        eval_path = path + "/%s_%s" % (metric, str(i))
        if not os.path.exists(eval_path):
            os.mkdir(eval_path)
        data = pd.read_csv(feature["data_set"])
        labels = data['label']
        urls = data['url']
        metric = feature["metric"]
        FeatureEvaluation(feature["path"], urls, labels, metric, eval_path)


main(sys.argv[1])
