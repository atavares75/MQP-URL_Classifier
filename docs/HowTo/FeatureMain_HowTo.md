# FeatureMain.py

The FeatureMain.py script takes in a JSON config file and evaluates the features through tests for independence and correlation and outputs the results to a csv and heat map.

# Config Format (JSON file)
```json
{
	"feature_set": [
		{
			"path": "../../config/feature_set/feature_config_categorical.json",
			"data_set": "../../data/full_5050_training_set.csv",
			"metric": "Chi-Squared"
		},
		{
			"path": "../../config/feature_set/feature_config_numerical.json",
			"data_set": "../../data/full_5050_training_set.csv",
			"metric": "F-Test"
		},
        {
			"path": "../../config/feature_set/feature_config_lexical.json",
			"data_set": "../../data/full_5050_training_set.csv",
			"metric": "Correlation"
		}
	]

}
```
* "feature_set" - list of feature sets to evaluate
* "path" - the path to the config file for a feature_set (See "config_format/feature_set_config_format.md" for more information)
* "data_set" - the path to the .csv file for the data set
* "metric"	- the metric the program will use to evaluate the features

Possible "metric" values are: chi2, f-value and correlation.  
Using Chi-Squared will run a chi-squared test on the features provided.
Using F-Test will run a ANOVA F-Value test on the features provided.
Using Correlation will produce a correlation heat map with the features provided.

# Command

python FeatureMain.py <json_file>

# Output

Output is structured in the output folder as  
  * {time} - FeatureEvaluation  
    * Run0  
    * Run1  
		
Within a RunX folder is report containing results of evaluation. If the metric is Chi-Squared or F-Test, a csv will be output
 with the results of the evaluation. If the metric is correlation a correlation heat map will be output.
