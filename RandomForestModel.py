# Robert Dwan

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold, RFECV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from FeatureExtraction import extractLexicalFeatures

# Read in csv
dataset = pd.read_csv('data/all_data_labeled.csv')

# Store URLs and their labels
urls = dataset.url
labels = dataset.label

normal = dataset.loc[dataset['label'] == 'Normal']
phish = dataset.loc[dataset['label'] == 'phish']
malware = dataset.loc[dataset['label'] == 'malware']
ransomware = dataset.loc[dataset['label'] == 'ransomware']
botnet = dataset.loc[dataset['label'] == 'BotnetC&C']

all_url = np.array(str)
all_label = np.array(str)

i = 0
while i < 34062:
	all_url = np.append(all_url, normal.at[i, 'url'])
	all_label = np.append(all_label, 'Normal')
	i += 1
print("Normal Done")

i = 0
while i < 10990:
	row = phish.loc[phish['num'] == i].index[0]
	all_url = np.append(all_url, phish.at[row, 'url'])
	all_label = np.append(all_label, 'phish')
	i += 1
print("Phishing Done")

i = 1
while i < 952:
	row = ransomware.loc[ransomware['num'] == i].index[0]
	all_url = np.append(all_url, ransomware.at[row, 'url'])
	all_label = np.append(all_label, 'ransomware')
	i += 1
print("Ransomware Done")		

i = 1
while i < 8146:
	row = botnet.loc[botnet['num'] == i].index[0]
	all_url = np.append(all_url, botnet.at[row, 'url'])
	all_label = np.append(all_label, 'BotnetC&C')
	i += 1
print("Botnet Done")		

i = 0
while i < 13974:
	row = malware.loc[malware['num'] == i].index[0]
	all_url = np.append(all_url, malware.at[row, 'url'])
	all_label = np.append(all_label, 'malware')
	i += 1
print("Malware Done")

# Extract some lexical features
features = extractLexicalFeatures(all_url)

#Convert to numpy arrays
feature = np.asarray(features)

feature_train, feature_test, label_train, label_test = train_test_split(feature, all_label, test_size=0.20, random_state=1436)

#create the classifier and tune the parameters (more on the documentations)
rf = RandomForestClassifier(n_estimators= 25, max_depth= None,max_features = 0.4,random_state= 11)

# selector = RFECV(rf, step=1, cv=5)
# selector = selector.fit(feature_train, label_train)
# e = selector.support_
# f = selector.score(feature_train, label_train)
# print(e)
# print(f)

#fit the data
rf.fit(feature_train, label_train)
print("training Done")
#make the prediction on the unseen data
prediction = rf.predict(feature_test) 
print("predicting Done")

# Statistics for the model

print(confusion_matrix(label_test, prediction))
print(classification_report(label_test, prediction))
print(accuracy_score(label_test, prediction))

# sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
# thresh = sel.fit_transform(feature)
#
# print(feature[0])
# print(thresh[0])

