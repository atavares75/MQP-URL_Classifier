import json
import sys
import uuid

import pandas as pd
import numpy as np
import os

from FeatureExtraction.FeatureExtraction import FeatureSet
from Metrics.VisualizeResults import FeaturePerformance


def main(json_file):
    with open(json_file) as jf:
        run = json.load(jf)

    data = pd.read_csv(run["data_set"])

    labels = data['label']
    urls = data['url']

    fs = FeatureSet(run["feature_set"], urls)

    fp = FeaturePerformance(fs, labels)

    f_test, p_tes = fp.calculateF_Value()
    chi_score, p_val = fp.calculateChiX_Score()
    mi = fp.calculateMutualInformation()

    feature_plots = fp.generateFeaturePlots(f_test, mi, chi_score)
    heat_map = fp.buildCorrelationHeatMap()

    path = "outputs/FeatureEvaluation"
    if not os.path.exists(path):
        os.mkdir(path)

    label = uuid.uuid4()
    file = open("%s/features_eval_%s.txt" % (path,label), "w")

    file.write("Features implemented: \n")
    for feature in fs.FeatureList:
        file.write(feature+"\n")

    file.write("\nF-Values: \n")
    for f in f_test:
        file.write(str(f)+"\n")

    file.write("\nChi2-Values\n")
    for c in chi_score:
        file.write(str(c)+"\n")

    file.write("Mutual Information Values")
    for m in mi:
        file.write(str(m)+"\n")

    feature_plots.savefig('%s/Feature-Plots.png' % path, bbox_inches='tight')
    heat_map.savefig('%s/HeatMap.png' % path, bbox_inches='tight')

    file.close()


main(sys.argv[1])
