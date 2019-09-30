# FeatureExtraction

The FeatureExtraction package takes in a JSON config file and generates the feature list for the data set.

# Config Format (JSON file)
```json
{
  "FeatureList": [
    {
      "Feature": "Length of path"
    },
    {
      "Feature": "Length of URL"
    },
    {
      "Feature": "Length of hostname"
    },
    {
      "Feature": "Number . in URL"
    }
  ]
}

```
* "FeatureList" - list of features
* "Feature" - the name of a feature from the feature list

Possible "Feature" values are: 

| Feature | Description |
|-------- |-----------|
|Length of URL |	The number of characters in the URL.
|Number of . In URL|	The number of periods in URL.
|Number of @ in URL |	The number of @ symbols in URL.
|Params in URL|	If there are parameters in the URL.
|Queries in URL|	If there are queries in the URL.
|Fragments in URL| 	If there are fragments in the URL.
|Entropy of hostname| 	The calculated entropy of the hostname.
|Check for Non Standard port |	Checks if URL connects to host server through non standard port. The standard ports for http and https are 80, 443, and 8080.
|Check Alexa Top 1 Million| 	Checks to see if domain name is in the Alexa Top 1 Million.
|Check for punycode |	Checks for presence of punycode in the URL.
|Check sub-domains| 	Checks the sub-domains of URL for names in the Alexa Top 1 Million.
|Check - in hostname |	If there us a - symbol in hostname.
|Digits in hostname |	If there are digits in the hostname.
|Length of hostname |	The number of characters in the hostname.
|Number of . in hostname|	The number of periods in the hostname
|IP based hostname|	Looks for IP address in hostname.
|Count % in url|	The number of % symbols in URL.
|Check TLD|	The Top Level Domain of URL.
|Length of path|	The number of characters in the path.
|Count - in path|	The number of - symbols in the path.
|Count / in path|	The number of / symbols in the path.
|Count = in path|	The number of = symbols in the path.
|Count ; in path|	The number of semi-colons in the path.
|Count , in path|	The number of commas in the path.
|Count _ in path|	The number of underscores in the path.
|Count . in path|	The number of periods in the path.
|Count & in path|	The number of ampersands in the path.
|Username/Password in URL|	If username or password is in URL.
|Check protocol|	If the URL protocol is https or not.
|IP address location|	The country the IP address comes from
|Address Registry|	The country the host is registered in.
|Days Registered|	The number of days the host has been registered for.

