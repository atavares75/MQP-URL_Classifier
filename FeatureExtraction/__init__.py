import io
import os
import zipfile

import pandas
import requests

zip_file_url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"


if not os.path.exist('data/top-1m.csv'):
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('data/')
d = pandas.read_csv('data/top-1m.csv', sep=',', header=None, names=['Domain'], index_col=0)
alexaDict = d.to_dict('list')
listOfDomains = list(alexaDict.values())
alexaSet = set(listOfDomains[0])
alexaNameSet = set()
for name in alexaSet:
    tokens = name.partition('.')
    alexaNameSet.add(tokens[0])

