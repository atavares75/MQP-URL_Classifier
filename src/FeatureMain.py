import json
import os
import sys
import uuid

import pandas as pd
from FeatureExtraction.FeatureExtraction import FeatureSet
from Metrics.FeaturePerformance import FeaturePerformance
from OutputGenerator.OutputGenerator import output_path
from pandas import DataFrame


class FeatureEvaluation:

    def __init__(self, feature_set_config_path, urls, labels, metric, path):
        fs = FeatureSet(feature_set_config_path, urls)

        fp = FeaturePerformance(fs, labels)

        label = uuid.uuid4()

        eval_path = path + "/%s_%s" % (metric, label)
        if not os.path.exists(eval_path):
            os.mkdir(eval_path)

        if metric == "correlation":
            heat_map = fp.buildCorrelationHeatMap()
            heat_map.savefig('%s/HeatMap.png' % eval_path, bbox_inches='tight')
            print(label)
            return

        file = open("%s/features_eval_%s.csv" % (eval_path, label), "w")

        if metric == "chi2":
            score, p_val = fp.calculateChiX_Score()
            score_name = "Chi-Score"
        if metric == "f-value":
            score, p_val = fp.calculateF_Value()
            score_name = "F-Value"

        df = DataFrame(columns=fs.FeatureList, index=[score_name, 'P-Value'])
        df.iloc[0] = score
        df.iloc[1] = p_val

        df.to_csv(file)

        file.close()
        print(label)


def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    label = uuid.uuid4()
    path = output_path + "/FeatureEvaluation_%s" % label
    if not os.path.exists(path):
        os.mkdir(path)

    for feature in run["feature_set"]:
        data = pd.read_csv(feature["data_set"])
        labels = data['label']
        urls = data['url']
        metric = feature["metric"]
        FeatureEvaluation(feature["path"], urls, labels, metric, path)


main(sys.argv[1])
