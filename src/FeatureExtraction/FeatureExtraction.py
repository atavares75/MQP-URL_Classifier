import json
import math
import re
from collections import Counter
from urllib.parse import urlparse

import tldextract
from pandas import DataFrame

from FeatureExtraction import alexaNameSet, alexaSet


class FeatureSet:
    """
    Class that constructs and contains feature data frame
    """

    def __init__(self, config_path, url_list):
        """
        Initialized parameters needed for the rest of the functions
        :param config_path: path to feature extraction configuration file
        :param url_list: list of urls as strings
        """
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
                    data_point.append(self.evaluateFeature(ex, feature))
            else:
                print(i)
                print(str(url))
            features.append(data_point)
        return DataFrame(features, columns=self.FeatureList)

    @staticmethod
    def evaluateFeature(ex, feature):
        """
        :param ex: Extractor instance
        :param feature: the feature you want evaluated
        :return: The output from extraction of selected feature
        """
        FeatureSwitcher = {'Length of URL': ex.checkLength(),
                           'Number of . in URL': ex.countCharacterInURL('.'),
                           'Number of @ in URL': ex.countCharacterInURL('@'),
                           'Count % in URL': ex.countCharacterInPath('%'),
                           'Params in URL': ex.checkForParams(),
                           'Queries in URL': ex.checkForQueries(),
                           'Fragments in URL': ex.checkForFragments(),
                           'Entropy of Domain name': ex.calculateEntropyOfDomainName(),
                           'Check for Non Standard port': ex.checkNonStandardPort(),
                           'Check Alexa Top 1 Million': ex.checkAlexaTop1Million(),
                           'Check for punycode': ex.checkForPunycode(),
                           'Check sub-domains': ex.checkSubDomains(),
                           '- in domain name': ex.checkForCharacterInHost('-'),
                           'Digits in domain name': ex.checkForDigitsInDomain(),
                           'Length of host': ex.checkLength(),
                           'Count . in domain name': ex.countCharacterInHost('.'),
                           'IP based host name': ex.checkForIPAddress(),
                           'Hex based host name': ex.checkHexBasedHost(),
                           'Check for common TLD': ex.checkTLD(),
                           'Length of path': ex.checkLength(),
                           'Count - in path': ex.countCharacterInPath('-'),
                           'Count / in path': ex.countCharacterInPath('/'),
                           'Count = in path': ex.countCharacterInPath('='),
                           'Count ; in path': ex.countCharacterInPath(';'),
                           'Count , in path': ex.countCharacterInPath(','),
                           'Count _ in path': ex.countCharacterInPath('_'),
                           'Count . in path': ex.countCharacterInPath('.'),
                           'Count & in path': ex.countCharacterInPath('&'),
                           'Username/Password in path': ex.checkForUsernameAndPassword(),
                           'Check URL protocol': ex.checkURLProtocol()
                           }
        return FeatureSwitcher[feature]


class Extractor:
    """
    Class that takes url and extracts features from it
    """

    def __init__(self, url):
        """
        Initializes parameters used by extractor functions
        :param url: a url as a string
        """
        self.URL = self.checkURLScheme(url)
        self.parseResults = urlparse(self.URL)
        if self.parseResults.hostname is None:
            self.parseResults.hostname = 'example'

    @staticmethod
    def checkURLScheme(url):
        """
        Checks URL scheme so that it can be properly processed by urlparse
        :param url: string
        :return: A properly formatted URL
        """
        tokens = url.partition('://')
        if len(tokens[1]) == 0:
            # no protocol in front of url
            return '//' + url
        else:
            return url

    def checkURLProtocol(self):
        """
        Checks if the URL protocol is https or not
        :return: 1 if not https, 0 if it is https
        """
        if self.parseResults.scheme is None:
            # protocol defaults to http
            return 1
        elif self.parseResults.scheme == 'https':
            # checks if URL uses secure connection
            return 0
        else:
            # if not https than it returns 1
            return 1

    def checkForCharacterInHost(self, character):
        """
        Checks for presence of character in url host name
        :param character: string
        :return: 1 if character is present, 0 if not
        """
        return 1 if character in self.parseResults.hostname else 0

    def checkForCharacterInPath(self, character):
        """
        Checks for presence of character in url path
        :param character: string
        :return: 1 if character is present, 0 if not
        """
        return 1 if character in self.parseResults.path else 0

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
        return sum(map(lambda x: 1 if character in x else 0, self.parseResults.hostname))

    def countCharacterInPath(self, character):
        """
        Counts instances if character in URL path
        :param character: string
        :return: int
        """
        return sum(map(lambda x: 1 if character in x else 0, self.parseResults.path))

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
        port = self.parseResults.port
        standardPorts = [80, 443, 8080]
        if port is not None:
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
        ext = tldextract.extract(self.parseResults.hostname)
        return 0 if ext.suffix in popularTLDs else 1

    def checkForIPAddress(self):
        """
        Checks for IP address in URL
        :return: 1 if IP address is in URL, 0 otherwise
        """
        regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', self.parseResults.hostname)
        return 1 if len(regex) > 0 else 0

    def checkForUsernameAndPassword(self):
        """
        Checks for username and password in URL
        :return: 2 if both keywords present, 1 if only one is present, 0 if neither
        """
        i = 0
        if self.parseResults.username is not None:
            i = i + 1
        if self.parseResults.password is not None:
            i = i + 1
        return i

    def calculateEntropyOfDomainName(self):
        """
        Calculates the entropy of the domain name
        :return: int
        """
        p, lengths = Counter(self.parseResults.hostname), float(len(self.parseResults.hostname))
        return -sum(count / lengths * math.log2(count / lengths) for count in p.values())

    def checkHexBasedHost(self):
        """
        Checks if host name is hex based
        :return: 1 if host name is hex based, 0 otherwise
        """
        try:
            int(self.parseResults.hostname, 16)
            return 1
        except ValueError:
            return 0

    def checkForDigitsInDomain(self):
        """
        Checks for digits in domain name
        :return: 1 if domain name contains digits, 0 otherwise
        """
        for c in self.parseResults.hostname:
            if c.isdigit():
                return 1
        return 0

    def checkAlexaTop1Million(self):
        """
        Checks if domain name is in the Alexa Top 1 Million
        :return: 1 if it is in the Alexa Top 1 Million, 0 otherwise
        """
        ext = tldextract.extract(self.parseResults.hostname)
        url = ext.domain + '.' + ext.suffix
        if url in alexaSet:
            return 1
        return 0

    def checkSubDomains(self):
        """
        Checks if the URL sub-domains are in the Alexa Top 1 Million
        :return: 1 if sub-domain is in Alexa Top 1 Million, 0 otherwise
        """
        ext = tldextract.extract(self.parseResults.hostname)
        sub_domains = ext.subdomain.split('.')
        for sub in sub_domains:
            if sub in alexaNameSet and sub != 'www':
                return 1
        return 0

    def checkForPunycode(self):
        """
        Checks for punycode in URL
        :return: 1 if puny code is present, 0 otherwise
        """
        if 'xn-' in self.parseResults.hostname:
            return 1
        return 0
