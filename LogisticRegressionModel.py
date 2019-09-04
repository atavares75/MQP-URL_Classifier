# Robert Dwan

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from FeatureExtraction import extractLexicalFeatures
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression

dataset = pd.read_csv("data/all_data_labeled.csv")

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values
features = extractLexicalFeatures(urls)

#Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(labels)

xTrain, xTest, yTrain, yTest = train_test_split(feature, ls, test_size = 0.25, random_state = 2)

lr = LogisticRegression(multi_class='multinomial', solver='lbfgs')

lr.fit(xTrain, yTrain)

prediction = lr.predict(xTest)

print(confusion_matrix(yTest, prediction))
print(classification_report(yTest, prediction))
print(accuracy_score(yTest, prediction))


