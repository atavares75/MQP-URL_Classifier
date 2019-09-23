import io
import os
import zipfile

import pandas
import requests

zip_file_url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"

if not os.path.exists('../../data/top-1m.csv'):
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall('../../data/')
d = pandas.read_csv('../../data/top-1m.csv', sep=',', header=None, names=['Domain'], index_col=0)
alexaDict = d.to_dict('list')
listOfDomains = list(alexaDict.values())
alexaSet = set(listOfDomains[0])
alexaNameSet = set()
for name in alexaSet:
    tokens = name.partition('.')
    alexaNameSet.add(tokens[0])


def functionSwitcher(ex, feature):
    """
    Returns tuple of method name and parameters
    :param ex: the url Extractor object
    :param feature: string representing the desired feature
    :return: tuple of method name and parameters
    """
    FeatureSwitcher = {'Length of URL': (ex.checkLengthOfURL, None),
                       'Number of . in URL': (ex.countCharacterInURL, {'character': '.'}),
                       'Number of @ in URL': (ex.countCharacterInURL, {'character': '@'}),
                       'Count % in URL': (ex.countCharacterInPath, {'character': '%'}),
                       'Params in URL': (ex.checkForParams, None),
                       'Queries in URL': (ex.checkForQueries, None),
                       'Fragments in URL': (ex.checkForFragments, None),
                       'Entropy of hostname': (ex.calculateEntropyOfDomainName, None),
                       'Check for Non Standard port': (ex.checkNonStandardPort, None),
                       'Check Alexa Top 1 Million': (ex.checkAlexaTop1Million, None),
                       'Check for punycode': (ex.checkForPunycode, None),
                       'Check sub-domains': (ex.checkSubDomains, None),
                       '- in hostname': (ex.checkForCharacterInHost, {'character': '-'}),
                       'Digits in hostname': (ex.checkForDigitsInDomain, None),
                       'Length of hostname': (ex.checkLengthOfHostname, None),
                       'Count . in hostname': (ex.countCharacterInHost, {'character': '.'}),
                       'IP based hostname': (ex.checkForIPAddress, None),
                       'Check TLD': (ex.checkTLD, None),
                       'Length of path': (ex.checkLengthOfPath, None),
                       'Count - in path': (ex.countCharacterInPath, {'character': '-'}),
                       'Count / in path': (ex.countCharacterInPath, {'character': '/'}),
                       'Count = in path': (ex.countCharacterInPath, {'character': '='}),
                       'Count ; in path': (ex.countCharacterInPath, {'character': ';'}),
                       'Count , in path': (ex.countCharacterInPath, {'character': ','}),
                       'Count _ in path': (ex.countCharacterInPath, {'character': '_'}),
                       'Count . in path': (ex.countCharacterInPath, {'character': '.'}),
                       'Count & in path': (ex.countCharacterInPath, {'character': '&'}),
                       'Username/Password in URL': (ex.checkForUsernameAndPassword, None),
                       'Check protocol': (ex.checkURLProtocol, None),
                       'IP address location': (ex.addressLocation, None),
                       'Address Registry': (ex.addressRegistry, None),
                       'Days Registered': (ex.dateRegistered, None)
                       }
    fun = FeatureSwitcher.get(feature)
    return fun
