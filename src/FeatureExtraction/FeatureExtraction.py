import json
import math
import re
import socket
from collections import Counter
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
import tldextract
from ipwhois.asn import IPASN
from ipwhois.net import Net
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder

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
        self.columnNames = self.FeatureList.copy()

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
                    fun = self.__functionSwitcher(ex, feature)
                    if fun is None:
                        continue
                    else:
                        method, params = fun
                    if params is None:
                        result = method()
                    else:
                        result = method(**params)
                    data_point.append(result)
            else:
                print(i)
                print(str(url))
            features.append(data_point)
        df = DataFrame(features, columns=self.FeatureList)
        obj_df = df.select_dtypes(include=['object']).copy()
        other_df = df.select_dtypes(exclude=['object']).copy()
        encoder = LabelEncoder()
        if not obj_df.empty:
            encoded_columns = encoder.fit_transform(obj_df).reshape(obj_df.to_numpy().shape)
            encoded_df = DataFrame(encoded_columns, columns=obj_df.columns)
        else:
            encoded_df = obj_df
        new_df = pd.concat([other_df, encoded_df], axis=1)
        self.columnNames = new_df.columns
        return new_df

    @staticmethod
    def __functionSwitcher(ex, feature):
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
                           'Entropy of Domain name': (ex.calculateEntropyOfDomainName, None),
                           'Check for Non Standard port': (ex.checkNonStandardPort, None),
                           'Check Alexa Top 1 Million': (ex.checkAlexaTop1Million, None),
                           'Check for punycode': (ex.checkForPunycode, None),
                           'Check sub-domains': (ex.checkSubDomains, None),
                           '- in domain name': (ex.checkForCharacterInHost, {'character': '-'}),
                           'Digits in domain name': (ex.checkForDigitsInDomain, None),
                           'Length of host': (ex.checkLengthOfHostname, None),
                           'Count . in domain name': (ex.countCharacterInHost, {'character': '.'}),
                           'IP based host name': (ex.checkForIPAddress, None),
                           'Hex based host name': (ex.checkHexBasedHost, None),
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
                           'Username/Password in path': (ex.checkForUsernameAndPassword, None),
                           'Check URL protocol': (ex.checkURLProtocol, None),
                           'IP Address Location': (ex.addressLocation, None),
                           'Address Registry': (ex.addressRegistry, None),
                           'Date Registered': (ex.dateRegistered, None)
                           }
        fun = FeatureSwitcher.get(feature)
        return fun


class Extractor:
    """
    Class that takes url and extracts features from it
    """
    results = None

    def __init__(self, url):
        """
        Initializes parameters used by extractor functions
        :param url: a url as a string
        """
        self.URL = self.checkURLScheme(url)
        self.parseResults = urlparse(self.URL)

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

    def checkLengthOfURL(self):
        """
        Calculates the length of the URL
        :return: int
        """
        return len(self.URL)

    def checkLengthOfHostname(self):
        """
        Calculates the length of the hostname
        :return: int
        """
        return len(self.parseResults.hostname)

    def checkLengthOfPath(self):
        """
        Calculates the length of the path
        :return: int
        """
        return len(self.parseResults.path)

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
        Checks Top Level Domain of the URL
        :return: the TLD, the string xxx if there is no TLD or the tldextract library can't extract it
        """
        ext = tldextract.extract(self.parseResults.hostname)
        if len(ext.suffix) == 0:
            return 'xxx'
        return ext.suffix

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

    def addressLocation(self):
        if self.results is None:
            try:
                ip = socket.gethostbyname(self.parseResults.hostname)
                net = Net(ip)
                obj = IPASN(net)
                self.results = obj.lookup()
                country = self.results['asn_country_code']
                return country
            except:
                return 0
        else:
            country = self.results['asn_country_code']
            return country

    def addressRegistry(self):
        if self.results is None:
            try:
                ip = socket.gethostbyname(self.parseResults.hostname)
                net = Net(ip)
                obj = IPASN(net)
                self.results = obj.lookup()
                registry = self.results['asn_registry']
                return registry
            except:
                return 0
        else:
            registry = self.results['asn_registry']
            return registry

    def dateRegistered(self):
        if self.results is None:
            try:
                ip = socket.gethostbyname(self.parseResults.hostname)
                net = Net(ip)
                obj = IPASN(net)
                self.results = obj.lookup()
                today = datetime.today()
                date_registered = datetime.strptime(self.results['asn_date'], '%Y-%m-%d')
                return (today - date_registered).days
            except:
                return 0
        else:
            today = datetime.today()
            date_registered = datetime.strptime(self.results['asn_date'], '%Y-%m-%d')
            return (today - date_registered).days
