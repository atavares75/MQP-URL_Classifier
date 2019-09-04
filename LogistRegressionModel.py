# Robert Dwan

import pandas as pd
from sklearn.model_selection import train_test_split
from FeatureExtraction import extractLexicalFeatures
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression

url_data = pd.read_csv("data/all_data_labeled.csv")

print('CSV read')
urls = url_data['url']
xData = extractLexicalFeatures(urls)
yData = url_data['label']

xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size = 0.25, random_state = 2)

lr = LogisticRegression()

lr.fit(xTrain, yTrain)

prediction = lr.predict(xTest)

print(confusion_matrix(yTest, prediction))
print(classification_report(yTest, prediction))
print(accuracy_score(yTest, prediction))


