import json
import sys
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

    print("HAVE JSON")

    print("HAVE ALGORITHMS")

    fs = FeatureSet(run["data_set"], urls)
    feature_set = np.asarray(fs.df)

    fp = FeaturePerformance(feature_set, urls)

    f_test, p_tes = fp.calculateF_Value()
    chi_score, p_val = fp.calculateChiX_Score()
    mi = fp.calculateMutualInformation()

    feature_plots = fp.generateFeaturePlots(f_test, mi, chi_score)
    heat_map = fp.buildCorrelationHeatMap()

    path = "outputs/FeatureEvaluation"
    os.mkdir(path)

    file = open("%s/features_used.txt" % path, "w")

    file.write("Features implemented: \n")
    file.write(*fs.FeatureList, sep="\n")
    file.write("\nF-Values: \n")
    file.write(*f_test, sep="\n")
    file.write("\nChi2-Values\n")
    file.write(*chi_score, sep="\n")
    file.write("Mutual Information Values")
    file.write(*mi, sep="\n")

    feature_plots.savefig('%s/Feature-Plots.png' % path, bbox_inches='tight')
    heat_map.savefig('%s/HeatMap.png' % path, bbox_inches='tight')

    file.close()


main(sys.argv[1])
