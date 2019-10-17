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
alexaDict = d.head(1000).to_dict('list')
listOfDomains = list(alexaDict.values())
alexaSet = set(listOfDomains[0])
alexaNameSet = set()
for name in alexaSet:
    tokens = name.partition('.')
    alexaNameSet.add(tokens[0])

from FeatureExtraction.Extractor import Extractor

def featureSwitcher(ex, feature):
    """
    Returns tuple of method name and parameters
    :param ex: the url Extractor object
    :param feature: string representing the desired feature
    :return: tuple of method name and parameters
    """
    FeatureSwitcher = {'Length of URL': (ex.checkLengthOfURL, None),
                       'Length of path': (ex.checkLengthOfPath, None),
                       'Length of hostname': (ex.checkLengthOfHostname, None),
                       'Number . in URL': (ex.countCharacterInURL, {'character': '.'}),
                       'Number @ in URL': (ex.countCharacterInURL, {'character': '@'}),
                       'Number % in URL': (ex.countCharacterInPath, {'character': '%'}),
                       'Number _ in URL': (ex.countCharacterInURL, {'character': '_'}),
                       'Number ~ in URL': (ex.countCharacterInURL, {'character': '~'}),
                       'Number & in URL': (ex.countCharacterInURL, {'character': '&'}),
                       'Number # in URL': (ex.countCharacterInURL, {'character': '#'}),
                       'Number - in hostname': (ex.checkForCharacterInHost, {'character': '-'}),
                       'Number . in hostname': (ex.countCharacterInHost, {'character': '.'}),
                       'Number - in path': (ex.countCharacterInPath, {'character': '-'}),
                       'Number / in path': (ex.countCharacterInPath, {'character': '/'}),
                       'Number = in path': (ex.countCharacterInPath, {'character': '='}),
                       'Number ; in path': (ex.countCharacterInPath, {'character': ';'}),
                       'Number , in path': (ex.countCharacterInPath, {'character': ','}),
                       'Number . in path': (ex.countCharacterInPath, {'character': '.'}),
                       'Params in URL': (ex.checkForParams, None),
                       'Queries in URL': (ex.checkForQueries, None),
                       'Fragments in URL': (ex.checkForFragments, None),
                       'Entropy of hostname': (ex.calculateEntropyOfDomainName, None),
                       'Check for Non Standard port': (ex.checkNonStandardPort, None),
                       'Check Alexa Top 1 Million': (ex.checkAlexaTop1Million, None),
                       'Check for punycode': (ex.checkForPunycode, None),
                       'Check sub-domains': (ex.checkSubDomains, None),
                       'Number digits in hostname': (ex.countDigitsInDomain, None),
                       'IP based hostname': (ex.checkForIPAddress, None),
                       'Check TLD': (ex.checkCommonTLD, None),
                       'Username/Password in URL': (ex.checkForUsernameAndPassword, None),
                       'Check protocol': (ex.checkURLProtocol, None),
                       'IP address location': (ex.addressLocation, None),
                       'Address Registry': (ex.addressRegistry, None),
                       'Days Registered': (ex.dateRegistered, None)
                       }
    fun = FeatureSwitcher.get(feature)
    return fun


def extractorSwitcher(extractor):
    """
    returns extractor class name as callable
    :param extractor: extractor class name
    :return:
    """
    ExtractorSwitcher = {
        'Extractor': Extractor
    }
    return ExtractorSwitcher.get(extractor)
