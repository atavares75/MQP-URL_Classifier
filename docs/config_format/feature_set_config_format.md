# FeatureExtraction

The FeatureExtraction package takes in a JSON config file and generates the feature list for the data set.

# Config Format (JSON file)
```json
{
  "Extractor": "Extractor",
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
* "Extractor" - the feature extractor class you would like to use. Default value is Extractor.
* "FeatureList" - list of features
* "Feature" - the name of a feature from the feature list

Possible "Feature" values are: 

| Feature | Description |
|-------- |-----------|
|	Length of URL |	The number of characters in the URL.
|	Length of hostname |	The number of characters in the hostname.
|	Length of path	|	The number of characters in the path.
|	Number . in URL	|	The number of periods in URL.
|	Number @ in URL |	The number of @ symbols in URL.
|	Number % in URL	|	The number of % symbols in URL.
|	Number _ in URL	|	The number of underscores in URL.
|	Number ~ in URL	|	The number of ~ in URL.
|	Number & in URL	|	The number of ampersands in URL.
|	Number # in URL	|	The number of # symbols in URL.
|	Number - in hostname |	The number of - symbol in hostname.
|	Number . in hostname |	The number of periods in the hostname
|	Number - in path |	The number of - symbols in the path.
|	Number / in path |	The number of / symbols in the path.
|	Number = in path |	The number of = symbols in the path.
|	Number ; in path |	The number of semi-colons in the path.
|	Number , in path |	The number of commas in the path.
|	Number . in path |	The number of periods in the path.
|	Params in URL |	If there are parameters in the URL.
|	Queries in URL |	If there are queries in the URL.
|	Fragments in URL |	If there are fragments in the URL.
|	Entropy of hostname |	The calculated entropy of the hostname.
|	Check for Non Standard port |	Checks if URL connects to host server through non standard port. The standard ports for http and https are 80, 443, and 8080.
|	Check Alexa Top 1 Million |	Checks to see if domain name is in the Alexa Top 1 Million.
|	Check for punycode |	Checks for presence of punycode in the URL.
|	Check sub-domains |	Checks the sub-domains of URL for names in the Alexa Top 1 Million.
|	Number digits in hostname |	The number of digits in the hostname.
|	IP based hostname |	Looks for IP address in hostname.
|	Check TLD |	Checks if the Top Level Domain of URL is common.
|	Username/Password in URL |	If username or password is in URL.
|	Check protocol |	If the URL protocol is https or not.
|	IP address location	|	The country the IP address comes from
|	Address Registry |	The country the host is registered in.
|	Days Registered	|	The number of days the host has been registered for.

