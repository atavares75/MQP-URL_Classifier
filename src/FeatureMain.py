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

    def __init__(self, feature_set_config_path, urls, labels, metric):
        fs = FeatureSet(feature_set_config_path, urls)

        fp = FeaturePerformance(fs, labels)

        label = uuid.uuid4()
        path = output_path + "/FeatureEvaluation_%s" % label
        if not os.path.exists(path):
            os.mkdir(path)

        heat_map = fp.buildCorrelationHeatMap()
        heat_map.savefig('%s/HeatMap.png' % path, bbox_inches='tight')

        file = open("%s/features_eval.csv" % path, "w")

        if metric == "chi2":
            score, p_val = fp.calculateChiX_Score()
            score_name = "Chi-Score"
        else:
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

    for feature in run["feature_set"]:
        data = pd.read_csv(feature["data_set"])
        labels = data['label']
        urls = data['url']
        metric = feature["metric"]
        FeatureEvaluation(feature["path"], urls, labels, metric)


main(sys.argv[1])
