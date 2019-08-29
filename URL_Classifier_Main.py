import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from FeatureExtraction import extractLexicalFeatures
from sklearn.tree import DecisionTreeClassifier
import sklearn.feature_extraction
import sklearn.feature_selection
import sklearn.model_selection
from sklearn import metrics
from sklearn.svm import LinearSVC

url_data = pd.read_csv("all_data_labeled.csv")

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

urls = url_data['url']
input = extractLexicalFeatures(urls)
output = url_data['label']

xTrain, xTest, yTrain, yTest = train_test_split(input, output, test_size = 0.25, random_state = 2)

svm = LinearSVC()



