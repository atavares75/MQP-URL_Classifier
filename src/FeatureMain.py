import json
import os
import sys
import uuid

import pandas as pd
from FeatureExtraction.FeatureExtraction import FeatureSet
from Metrics.VisualizeResults import FeaturePerformance
from pandas import DataFrame


class FeatureEvaluation:

    def __init__(self, feature_set_config_path, urls, labels):
        fs = FeatureSet(feature_set_config_path, urls)

        fp = FeaturePerformance(fs, labels)

        f_test, p_tes = fp.calculateF_Value()
        chi_score, p_val = fp.calculateChiX_Score()
        mi = fp.calculateMutualInformation()

        label = uuid.uuid4()
        path = "../outputs/FeatureEvaluation_%s" % label
        if not os.path.exists(path):
            os.mkdir(path)

        heat_map = fp.buildCorrelationHeatMap()
        heat_map.savefig('%s/HeatMap.png' % path, bbox_inches='tight')

        file = open("%s/features_eval.csv" % path, "w")

        df = DataFrame(columns=fs.FeatureList, index=['F-Values', 'Chi2-Score', 'P-Value', 'Mutual Info Values'])
        df.iloc[0] = f_test
        df.iloc[1] = chi_score
        df.iloc[2] = p_val
        df.iloc[3] = mi

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
        FeatureEvaluation(feature["path"], urls, labels)


main(sys.argv[1])
