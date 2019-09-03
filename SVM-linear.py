import pandas as pd
from sklearn.model_selection import train_test_split
from FeatureExtraction import extractLexicalFeatures
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC
import numpy as np

dataset = pd.read_csv("data/all_data_labeled.csv")

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values
features = extractLexicalFeatures(urls)

#Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(labels)

# #Reshape the arrays for SKLearn functions
# feature = np.reshape(feature, (-1,3))
# ls = np.reshape(ls, (-1,1))

print('Features Extracted')

xTrain, xTest, yTrain, yTest = train_test_split(feature, ls, test_size = 0.25, random_state = 2)
print('\nTraining data split\n')


svm = LinearSVC(dual=False, fit_intercept=False, max_iter=2000)
print('\nModel Created\n')

svm.fit(xTrain, yTrain)
print('\nModel Fitted\n')

prediction = svm.predict(xTest)
print('\nPrediction finished\n')

print('\nPrediction Data\n')
print(prediction)
print('\nTest Data\n')
print(yTest)

print(confusion_matrix(yTest, prediction))
print(classification_report(yTest, prediction))
print(accuracy_score(yTest, prediction))
print('\nMetrics calculated\n')

