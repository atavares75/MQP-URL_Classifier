import pandas as pd
from sklearn.model_selection import train_test_split
from FeatureExtraction import extractLexicalFeatures
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import SVC
import numpy as np
from sklearn.model_selection import cross_val_score

dataset = pd.read_csv("data/all_data_labeled.csv")

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values
features = extractLexicalFeatures(urls)

#Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(labels)

xTrain, xTest, yTrain, yTest = train_test_split(feature, ls, test_size=0.6, random_state=11)

svm = SVC(kernel='rbf', gamma='auto', max_iter=10000, C=1)

svm.fit(xTrain, yTrain)

prediction = svm.predict(xTest)

print(confusion_matrix(yTest, prediction))
print(classification_report(yTest, prediction))
print(accuracy_score(yTest, prediction))