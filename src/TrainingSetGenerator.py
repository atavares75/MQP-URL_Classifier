# Robert Dwan

import pandas as pd
import random
import sys

if len(sys.argv) != 6:
	print("Invalid Input.")
	print("Ex. TrainingSetDenerator.py <# normal> <# phishing> <# malware> <# ransomware> <# botnet>")
	sys.exit()

classes = ['Normal', 'phishing', 'malware', 'ransomware', 'botnet']

training_set = []

def get_urls(label, wanted):
	filename = "data/%s_training_set.csv" % label
	rows = sum(1 for line in open(filename, encoding = 'utf-8')) - 1 
	skip = sorted(random.sample(range(1, rows + 1), rows - wanted))
	df = pd.read_csv(filename, skiprows = skip, encoding = 'utf-8')
	training_set.append(df)

i = 1
for type in classes:
	get_urls(type, int(sys.argv[i]))
	i = i + 1

final_df = pd.concat(training_set, axis = 0, ignore_index = True)
final_df.to_csv('data/new_training_set.csv', sep = ',', encoding = 'utf-8')
