# Main.py

The Main.py script takes in a JSON config file and performs batch runs and produces output.

# Config Format (JSON file)
```json
{ 
	"runs": [{
		"algorithm": "../../config/algorithm_config.json",
		"feature_set": "../../config/feature_config_lexical.json",
		"training_set": "../../data/full_5050_training_set.csv",
		"testing_set": "../../data/labeled_test_set.csv",
		"metric": "accuracy"
	},
	{
		"algorithm": "../../config/algorithm_config.json",
		"feature_set": "../../config/feature_config_lexical.json",
		"training_set": "../../data/5050_training_set.csv",
		"testing_set": "../../data/labeled_test_set.csv",
		"metric": "accuracy"
	}]	
}
```
* "runs" - list of algorithms to run
* "algorithm" - the path to the config file for an algorithm (See "algorithm_config_format.md" for more information)
* "feature_set" - the path to the config file for a feature_set (See "feature_set_config_format.md" for more information)
* "training_set" - the path to the .csv file for the training data set
* "testing_set" - the path to the .csv file for the testing data set
* "metric" - the metric 

# Command

python Main.py <json_file>
