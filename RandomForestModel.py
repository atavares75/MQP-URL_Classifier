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
urls = dataset.iloc[:, 2].values
labels = dataset.iloc[:, 1].values

# Extract some lexical features
features = extractLexicalFeatures(urls)

#Convert to numpy arrays
feature = np.asarray(features)
ls = np.asarray(labels)


feature_train, feature_test, label_train, label_test = train_test_split(feature, ls, test_size=0.20, random_state=1436)

#create the classifier and tune the parameters (more on the documentations)
rf = RandomForestClassifier(n_estimators= 25, max_depth= None,max_features = 0.4,random_state= 11)

selector = RFECV(rf, step=1, cv=5)
selector = selector.fit(feature_train, label_train)
e = selector.support_
f = selector.score(feature_train, label_train)
print(e)
print(f)

#fit the data
rf.fit(feature_train, label_train)

#make the prediction on the unseen data
prediction = rf.predict(feature_test) 


# Statistics for the model

print(confusion_matrix(label_test, prediction))
print(classification_report(label_test, prediction))
print(accuracy_score(label_test, prediction))

sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
thresh = sel.fit_transform(feature)

print(feature[0])
print(thresh[0])

