# Robert Dwan

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Read in csv
dataset = pd.read_csv('data\\all_data_labeled.csv')

# Store URLs and their labels
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values

features = []
lab = []

i = 0

# Extract some lexical features
for url in urls:
	i = i + 1
	if type(url) is str:
		features.append([len(url), len(url.split('/')[0]), len(url.split('.')) - 1])
	else:
		print(i)
		print(str(url))

#Covert benign URLs to 0 and malicious to 1		
for label in labels:
	if label == 'Normal':
		lab.append(0)
	else:
		lab.append(1)

#Add a missing feature, looking into problem - 288543 is missing a URL
#features.append([13, 9, 6])

#Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(lab)

#Reshape the arrays for SKLearn functions
feature = np.reshape(feature, (-1,3))
ls = np.reshape(ls, (-1,1))

from sklearn.model_selection import train_test_split
feature_train, feature_test, label_train, label_test = train_test_split(feature, ls, test_size=0.25, random_state=2)

#create the classifier and tune the parameters (more on the documentations)
rf = RandomForestClassifier(n_estimators= 25, max_depth= None,max_features = 0.4,random_state= 11 )

#fit the data
rf.fit(feature_train, label_train)

#make the prediction on the unseen data
prediction = rf.predict(feature_test) 


# Statistics for the model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(label_test, prediction))
print(classification_report(label_test, prediction))
print(accuracy_score(label_test, prediction))

