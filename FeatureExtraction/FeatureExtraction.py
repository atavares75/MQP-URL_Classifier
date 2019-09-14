import json
import math
import re
from collections import Counter
from urllib.parse import urlparse

import tldextract
from pandas import DataFrame

from FeatureExtraction import alexaNameSet, alexaSet


def evaluateFeature(ex, feature):
    """
    :param ex: Extractor instance
    :param feature: the feature you want evaluated
    :return: The output from extraction of selected feature
    """
    FeatureSwitcher = {'Length of URL': ex.checkLength(),
                       'Number of ‘.’ in URL': ex.countCharacterInURL('.'),
                       'Number of ‘@‘ in URL': ex.countCharacterInURL('@'),
                       'Params in URL': ex.checkForParams(),
                       'Queries in URL': ex.checkForQueries(),
                       'Fragments in URL': ex.checkForFragments(),
                       'Entropy of Domain name': ex.calculateEntropyOfDomainName(),
                       'Check for Non Standard port': ex.checkNonStandardPort(),
                       'Check Alexa Top 1 Million': ex.checkAlexaTop1Million(),
                       'Check for punycode': ex.checkForPunycode(),
                       'Check sub-domains': ex.checkSubDomains(),
                       '’-‘ in domain name': ex.checkForCharacterInHost('-'),
                       'Digits in domain name': ex.checkForDigitsInDomain(),
                       'Length of host': ex.checkLength(),
                       'Count ‘.’ in domain name': ex.countCharacterInHost('.'),
                       'IP based host name': ex.checkForIPAddress(),
                       'Hex based host name': ex.checkHexBasedHost(),
                       'Check for common TLD': ex.checkTLD(),
                       'Length of path': ex.checkLength(),
                       'Count ‘-‘ in path': ex.countCharacterInPath('-'),
                       'Count ‘/‘ in path': ex.countCharacterInPath('/'),
                       'Count ‘=‘ in path': ex.countCharacterInPath('='),
                       'Count ‘;‘ in path': ex.countCharacterInPath(';'),
                       'Count ‘,‘ in path': ex.countCharacterInPath(','),
                       'Count ‘_‘ in path': ex.countCharacterInPath('_'),
                       'Count ‘.’ in path': ex.countCharacterInPath('.'),
                       'Count ‘?’ in path': ex.countCharacterInPath('?'),
                       'Count ‘&’ in path': ex.countCharacterInPath('&'),
                       'Username/Password in path': ex.checkForUsernameOrPassword()
                       }
    return FeatureSwitcher[feature]


class FeatureSet:
    """
    Class that constructs and contains feature data frame
    """

    def __init__(self, config_path, url_list):
        with open(config_path) as fe:
            selectedFeatures = json.load(fe)
        self.FeatureList = list()
        for feature in selectedFeatures["FeatureList"]:
            self.FeatureList.append(feature["Feature"])
        self.df = self.__extractFeatures(url_list)

    def __extractFeatures(self, url_list):
        """
        From the list of features defined in config file it generates feature set
        :param url_list: list of URLs as strings
        :return: A panda DataFrame containing features of each URL
        """
        features = list()
        i = 0
        for url in url_list:
            i = i + 1
            data_point = list()
            if type(url) is str:
                ex = Extractor(url)
                for feature in self.FeatureList:
                    data_point.append(evaluateFeature(ex, feature))
            else:
                print(i)
                print(str(url))
            features.append(data_point)
        return DataFrame(features, columns=self.FeatureList)


class Extractor:
    """
    Class that takes url and extracts features from it
    """

    def __init__(self, url):
        self.URL = self.checkURLScheme(url)
        self.parseResults = urlparse(self.URL)
        self.path = self.parseResults.path
        self.host = self.parseResults.netloc

    def checkURLScheme(self, url):
        """
        Checks URL scheme so that it can be properly processed by urlparse
        :param url: string
        :return: A properly formatted URL
        """
        tokens = self.URL.partition('://')
        if len(tokens[1]) == 0:
            # no protocol in front of url
            return '//' + url
        else:
            return url

    def checkForCharacterInHost(self, character):
        """
        Checks for presence of character in url host name
        :param character: string
        :return: 1 if character is present, 0 if not
        """
        return 1 if character in self.host else 0

    def checkForCharacterInPath(self, character):
        """
        Checks for presence of character in url path
        :param character: string
        :return: 1 if character is present, 0 if not
        """
        return 1 if character in self.path else 0

    def countCharacterInURL(self, character):
        """
        Counts instances if character in URL
        :param character: string
        :return: int
        """
        return sum(map(lambda x: 1 if character in x else 0, self.URL))

    def countCharacterInHost(self, character):
        """
        Counts instances if character in URL host name
        :param character: string
        :return: int
        """
        return sum(map(lambda x: 1 if character in x else 0, self.host))

    def countCharacterInPath(self, character):
        """
        Counts instances if character in URL path
        :param character: string
        :return: int
        """
        return sum(map(lambda x: 1 if character in x else 0, self.path))

    def checkLength(self):
        """
        Calculates the length of the URL
        :return: int
        """
        return len(self.URL)

    def checkNonStandardPort(self):
        """
        Checks if URL uses a non-standard port
        :return: 1 if non-standard port, 0 otherwise
        """
        port = self.host.rpartition(':')[2]
        standardPorts = ['80', '443', '8080']
        if len(port) > 0 and port.isdigit():
            if port in standardPorts:
                return 0
            else:
                return 1
        else:
            return 0

    def checkForFragments(self):
        """
        Checks for fragments in URL
        :return: 1 if fragments in URL, 0 otherwise
        """
        return 1 if len(self.parseResults.fragment) > 0 else 0

    def checkForQueries(self):
        """
        Checks for queries in URL
        :return: 1 if queries in URL, 0 otherwise
        """
        return 1 if len(self.parseResults.query) > 0 else 0

    def checkForParams(self):
        """
        Checks for parameters in URL
        :return: 1 if parameters in URL, 0 otherwise
        """
        return 1 if len(self.parseResults.params) > 0 else 0

    def checkTLD(self):
        """
        Checks if URL TLD is a common TLD ('com', 'net', 'gov', 'edu', 'org', 'de')
        :return: 1 if not a common TLD, 0 otherwise
        """
        popularTLDs = ['com', 'net', 'gov', 'edu', 'org', 'de']
        ext = tldextract.extract(self.host)
        return 0 if ext.domain in popularTLDs else 1

    def checkForIPAddress(self):
        """
        Checks for IP address in URL
        :return: 1 if IP address is in URL, 0 otherwise
        """
        regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', self.URL)
        return 1 if regex is not None else 0

    def checkForUsernameOrPassword(self):
        """
        Checks for 'username' and 'password' keywords in URL
        :return: 2 if both keywords present, 1 if only one is present, 0 if neither
        """
        lowerPath = self.path.lower()
        i = 0
        if 'username' in lowerPath:
            i = i + 1
        if 'password' in lowerPath:
            i = i + 1
        return i

    def calculateEntropyOfDomainName(self):
        """
        Calculates the entropy of the domain name
        :return: int
        """
        p, lengths = Counter(self.host), float(len(self.host))
        return -sum(count / lengths * math.log2(count / lengths) for count in p.values())

    def checkHexBasedHost(self):
        """
        Checks if host name is hex based
        :return: 1 if host name is hex based, 0 otherwise
        """
        try:
            int(self.URL, 16)
            return 1
        except ValueError:
            return 0

    def checkForDigitsInDomain(self):
        """
        Checks for digits in domain name
        :return: 1 if domain name contains digits, 0 otherwise
        """
        for c in self.URL:
            if c.isdigit():
                return 1
        return 0

    def checkAlexaTop1Million(self):
        """
        Checks if domain name is in the Alexa Top 1 Million
        :return: 1 if it is in the Alexa Top 1 Million, 0 otherwise
        """
        ext = tldextract.extract(self.host)
        url = ext.domain + '.' + ext.suffix
        if url in alexaSet:
            return 1
        return 0

    def checkSubDomains(self):
        """
        Checks if the URL sub-domains are in the Alexa Top 1 Million
        :return: 1 if sub-domain is in Alexa Top 1 Million, 0 otherwise
        """
        ext = tldextract.extract(self.host)
        sub_domains = ext.subdomain.split('.')
        for sub in sub_domains:
            if sub in alexaNameSet:
                return 1
        return 0

    def checkForPunycode(self):
        """
        Checks for punycode in URL
        :return: 1 if puny code is present, 0 otherwise
        """
        if 'xn--' in self.host:
            return 1
        return 0

# For Testing functions:
# extractLexicalFeatures(['www.goog-le.com/about', 'http://amazon.org/yep'])
# getURLScheme('https://www.goog-le.com/about')
# print(checkForIPAdress('https://www.2345.3453.222.3454.com/about'))
# checkAlexaTop1Million('www.google.co.uk')
# dataset = pd.read_csv("data/all_data_labeled.csv")

# Store URLs and their labels
# urls = dataset.iloc[:, 2].values
# checkForPunycode(urls[1])
