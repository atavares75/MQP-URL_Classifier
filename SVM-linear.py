import pandas as pd
from sklearn.model_selection import train_test_split
from FeatureExtraction import extractLexicalFeatures
import sklearn.feature_extraction
import sklearn.feature_selection
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC

url_data = pd.read_csv("data/all_data_labeled.csv")

# normal_data = url_data[url_data.label == 'Normal']
# phish_data = url_data[url_data.label == 'phish']
# malware_data = url_data[url_data.label == 'malware']
# ransomware_data = url_data[url_data.label == 'ransomware']
# botnet_data = url_data[url_data.label == 'BotnetC&C']
#
# print(normal_data)
# print(phish_data)
# print(malware_data)
# print(ransomware_data)
# print(botnet_data)
print('CSV read')
urls = url_data['url']
xData = extractLexicalFeatures(urls)
yData = url_data['label']
print('Features Extracted')

xTrain, xTest, yTrain, yTest = train_test_split(xData, yData, test_size = 0.25, random_state = 2)
print('\nTraining data split\n')
# print(xTrain)
# print(yTrain)
# print('-------------------------')
# print(xTest)
# print(yTest)

svm = LinearSVC(max_iter=1500)
print('\nModel Created\n')
#example parameters
#penalty=’l2’, loss=’squared_hinge’, dual=True, tol=0.0001, C=1.0, multi_class=’ovr’, fit_intercept=True, intercept_scaling=1, class_weight=None, verbose=0, random_state=None, max_iter=1000

svm.fit(xTrain, yTrain)
print('\nModel Fitted\n')

prediction = svm.predict(xTest)
print('\nPrediction finished\n')

print(confusion_matrix(yTest, prediction))
print(classification_report(yTest, prediction))
print(accuracy_score(yTest, prediction))
print('\nMetrics calculated\n')

