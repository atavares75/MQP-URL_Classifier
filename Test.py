# Robert Dwan

import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from FeatureExtraction import extractLexicalFeatures

algorithms = ["rf", "lr", "svm-l", "svm-rbf"]

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

def machine_learning_algorithm(input):
	switcher = {
	"rf" : RandomForestClassifier(n_estimators= 25, max_depth= None,max_features = 0.4,random_state= 11),
	"lr" : LogisticRegression(multi_class='multinomial', solver='lbfgs'),
	"svm-l" : LinearSVC(dual=False, fit_intercept=False, max_iter=1700, C=1),
	"svm-rbf" : SVC(kernel='rbf', gamma='auto', max_iter=100000, C=1)
	}
	return switcher.get(input, lambda: "Invalid Algorithm")
	
def train_and_test(algorithm):
	#a = algorithm
	algorithm.fit(feature_train, label_train)
	prediction = algorithm.predict(feature_test)

	print(confusion_matrix(label_test, prediction))
	print(classification_report(label_test, prediction))
	print(accuracy_score(label_test, prediction))
	
if (len(sys.argv) > 1):	
	train_and_test(machine_learning_algorithm(sys.argv[1]))
else:
	for algo in algorithms:
		train_and_test(machine_learning_algorithm(algo))
	
