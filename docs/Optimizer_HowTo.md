# Optimizer.py

The Optimizer.py script takes in a JSON config file and performs runs on an algorithm with one or two parameters being varied. The script produces the results for each run and a .txt file with the best performance based on the metric provided in the config.

# Config Format

{ 
	"algorithm": "RandomForest",
	"tuning_param": ["n_estimators", "random_state"],
	"parameters": {
		"min_samples_split": 2
	},
	"max": [25, 5],
	"min": [24, 4],
	"step": [1, 1],
	"feature_set": "../../config/feature_config_lexical.json",
	"training_set": "../../data/full_5050_training_set.csv",
	"testing_set": "../../data/labeled_test_set.csv",
	"metric": "accuracy"
}

"algorithm"	- the name of the algorithm to be run and tested
"tuning_param"	- List of parameters that will be varied in the run
"parameters"	- Other parameters for the algorithm that are not varied
"max"		- list of max values for the tuning parameters
"min"		- list of min values for the tuning parameters
"step"		- list of values the tuning parameter will increment by
"feature_set"	- path to the config file for the feature_set - see "feature_set_config.md" for more details
"training_set"	- path to the csv file that contains the training data set
"testing_set"	- path to the csv file that contains the testing data set
"metric"	- the metric that the user specifies and will be outputted to a separate txt file

Possible "metric" values are: accuracy, false_positive, and false_negative.
using accuracy will provide the parameters that produce the greatest accuracy.
Using false_positive or false_negative will provide the parameters that produce the lowest average rate for the metric.

# Command

python Optimizer.py <json_file>
