# Algorithm Configuration

The AlgorithmFactory takes a config file to create the machine learning models.

# Config Format (JSON file)
```json
{ 
	"algorithms": [{
		"algorithm": "RandomForest",
		"parameters": {
			"n_estimators": 40,
			"random_state": 11,
			"verbose": 100
		}
	}, {
		"algorithm": "LogisticRegression",
		"parameters": {
			"solver": "lbfgs",
			"max_iter": 10000,
			"multi_class": "multinomial",
			"verbose": 100
		}
	}, {
		"algorithm": "SVM-L",
		"parameters": {
			"dual": false,
			"max_iter": 30,
			"verbose": 100
		}
	}, {	
		"algorithm": "SVM-RBF",
		"parameters": {
			"max_iter": 10000,
			"gamma": 0.9,
			"verbose": 100
		}
	}]
}
```
* "algorithms" - list of algorithms to be run
* "algorithm" - the name of the algorithm
* "parameters" - the parameters for the algorithm

Possible "algorithm" values are: 

* RandomForest
* LogisticRegression
* SVM-L (Support Vector Machine with linear kernel)
* SVM-RBF (Support Vector Machine with Radial Basis Function kernel)