import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold, RFECV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from FeatureExtraction import extractLexicalFeatures

dataset = pd.read_csv("data/all_data_labeled.csv")

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values
features = extractLexicalFeatures(urls)

#Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(labels)

xTrain, xTest, yTrain, yTest = train_test_split(feature, ls, test_size=0.5, random_state=11)


svm = LinearSVC(dual=False, fit_intercept=False, max_iter=1700, C=1)

selector = RFECV(svm, step=1, cv=5)
selector = selector.fit(xTrain, yTrain)
e = selector.support_
f = selector.score(xTrain, yTrain)
print(e)
print(f)

svm.fit(xTrain, yTrain)

prediction = svm.predict(xTest)


print(confusion_matrix(yTest, prediction))
print(classification_report(yTest, prediction))
print(accuracy_score(yTest, prediction))

