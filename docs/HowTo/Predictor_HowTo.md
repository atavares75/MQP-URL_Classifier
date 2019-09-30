# Predictor.py

The Predictor.py script takes in a JSON config file containing a model, testing set, and a feature set. The script produces predictions on the testing set. The feature set must be the same as the original model was trained on.

# Config Format (JSON file)
```json
{
	"name": "RandomForest",
	"model": "../../models/model.joblib",
	"feature_set": "../../config/feature_config_lexical.json",
	"testing_set": "../../data/labeled_test_set.csv"
}
```
* "name"	- the name of the algorithm to be run and tested
* "model"	- the existing model to be retrained. (Must be a .joblib file)
* "feature_set"	- path to the config file for the feature_set - (See "config_format/feature_set_config.md" for more details)
* "testing_set"	- path to the csv file that contains the testing data set

# Command

python Predictor.py <json_file>
