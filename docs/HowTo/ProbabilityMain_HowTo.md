# ProbabilityMain.py

The ProbabilityMain.py script takes in a JSON config file and performs batch runs and outputs the predicted class probabilities above a given threshold.

# Config Format (JSON file)
```json
{ 
	"runs": [{
		"algorithm": "../../config/algorithm_config.json",
		"feature_set": "../../config/feature_config_lexical.json",
		"training_set": "../../data/full_5050_training_set.csv",
		"testing_set": "../../data/labeled_test_set.csv",
		"metric": "accuracy",
        "threshold": 0.30
	},
	{
		"algorithm": "../../config/algorithm_config.json",
		"feature_set": "../../config/feature_config_lexical.json",
		"training_set": "../../data/5050_training_set.csv",
		"testing_set": "../../data/labeled_test_set.csv",
		"metric": "accuracy",
        "threshold": 0.30
	}]	
}
```
* "runs" - list of algorithms to run
* "algorithm" - the path to the config file for an algorithm (See "config_format/algorithm_config_format.md" for more information)
* "feature_set" - the path to the config file for a feature_set (See "config_format/feature_set_config_format.md" for more information)
* "training_set" - the path to the .csv file for the training data set
* "testing_set" - the path to the .csv file for the testing data set
* "metric"	- the metric that the user specifies and will be outputted to a separate txt file
* "threshold" - the threshold probability value necessary for a URL to be tagged as certain class

Possible "metric" values are: accuracy, false_positive, and false_negative.  
using accuracy will provide the parameters that produce the greatest accuracy.  
Using false_positive or false_negative will provide the parameters that produce the lowest average rate for the metric.  

The algorithm(s) used must have a function called predict_proba() that outputs predicted class probabilities.

# Command

python ProbabilityMain.py <json_file>

# Output

Output is structured in the output folder as  
  * {time} - PredictionRun  
    * Run0  
    * Run1  
		
Within a RunX folder is the model, the list of false positives, false negatives, true positives, and true negatives, the metric report txt file, and the ROC curve.  
Within a {time} - BatchRun folder is a .txt file containing the "metric" values from the configuration, a .txt file containing the false tags, and a .csv containing the tags for each url.
