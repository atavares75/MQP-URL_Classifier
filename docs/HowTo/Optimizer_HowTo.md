# Optimizer.py

The Optimizer.py script takes in a JSON config file and performs runs on an algorithm with one or two parameters being varied. The script produces the results for each run and a .txt file with the best performance based on the metric provided in the config.

# Config Format (JSON file)
```json
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
```
* "algorithm"	- the name of the algorithm to be run and tested
* "tuning_param"	- List of parameters that will be varied in the run
* "parameters"	- Other parameters for the algorithm that are not varied
* "max"		- list of max values for the tuning parameters
* "min"		- list of min values for the tuning parameters
* "step"		- list of values the tuning parameter will increment by
* "feature_set"	- path to the config file for the feature_set - (See "config_format/feature_set_config.md" for more details)
* "training_set"	- path to the csv file that contains the training data set
* "testing_set"	- path to the csv file that contains the testing data set
* "metric"	- the metric that the user specifies and will be outputted to a separate text file

Possible "metric" values are: accuracy, false_positive, and false_negative.  
using accuracy will provide the parameters that produce the greatest accuracy.  
Using false_positive or false_negative will provide the parameters that produce the lowest average rate for the metric.  

# Command

python Optimizer.py <json_file>

# Output

For 1 Dimensional Optimization
Output is structured in the output folder as  
  * {time} - OptimizedRun  
    * AlgorithmName_TuningParamValue  
    * AlgorithmName_TuningParamValue  
		
Within a RunX folder is the list of false positives, false negatives, true positives, and true negatives, the metric report txt file, and the ROC curve.  
Within a {time} - Optimized folder is a .txt file containing the "metric" values from the configuration, the optimized model,
a line graph generated from the results, and a .csv file with the results.

For 2 Dimensional Optimization
Output is structured in the output folder as  
  * {time} - OptimizedRun  
    * AlgorithmName_FirstTuningParamValue_SecondTuningParamValue 
    * AlgorithmName_FirstTuningParamValue_SecondTuningParamValue  
		
Within a RunX folder is the list of false positives, false negatives, true positives, and true negatives, the metric report txt file, and the ROC curve.  
Within a {time} - Optimized folder is a .txt file containing the "metric" values from the configuration, the optimized model,
a heat map generated from the results, and a .csv file with the results.

