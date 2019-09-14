import json
import math
import re
from collections import Counter
from urllib.parse import urlparse
import tldextract
from pandas import DataFrame
from AlexaTop1MillionDict import alexaSet, alexaNameSet


def evaluateFeature(ex, feature):
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

    def __init__(self, path):
        with open(path) as fe:
            selectedFeatures = json.load(fe)
        self.FeatureList = list(selectedFeatures["FeatureList"].values())

    def extractLexicalFeatures(self, url_list):
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
        df = DataFrame(features, columns=self.FeatureList)
        return df


class Extractor:

    def __init__(self, url):
        self.URL = self.checkURLScheme(url)
        self.parseResults = urlparse(self.URL)
        self.path = self.parseResults.path
        self.host = self.parseResults.netloc

    def checkURLScheme(self, url):
        tokens = self.URL.partition('://')
        if len(tokens[1]) == 0:
            # no protocol in front of url
            return '//' + url
        else:
            return url

    def checkForCharacterInHost(self, character):
        return 1 if character in self.host else 0

    def checkForCharacterInPath(self, character):
        return 1 if character in self.path else 0

    def countCharacterInURL(self, character):
        return sum(map(lambda x: 1 if character in x else 0, self.URL))

    def countCharacterInHost(self, character):
        return sum(map(lambda x: 1 if character in x else 0, self.host))

    def countCharacterInPath(self, character):
        return sum(map(lambda x: 1 if character in x else 0, self.path))

    def checkLength(self):
        return len(self.URL)

    def checkNonStandardPort(self):
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
        return 1 if len(self.parseResults.fragment) > 0 else 0

    def checkForQueries(self):
        return 1 if len(self.parseResults.query) > 0 else 0

    def checkForParams(self):
        return 1 if len(self.parseResults.params) > 0 else 0

    def checkTLD(self):
        popularTLDs = ['com', 'net', 'gov', 'edu', 'org', 'de']
        ext = tldextract.extract(self.host)
        return 0 if ext.domain in popularTLDs else 1

    def checkForIPAddress(self):
        regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', self.URL)
        return 1 if regex is not None else 0

    def checkForUsernameOrPassword(self):
        lowerPath = self.path.lower()
        i = 0
        if 'username' in lowerPath:
            i = i + 1
        if 'password' in lowerPath:
            i = i + 1
        return i

    def calculateEntropyOfDomainName(self):
        p, lengths = Counter(self.host), float(len(self.host))
        return -sum(count / lengths * math.log2(count / lengths) for count in p.values())

    def checkHexBasedHost(self):
        try:
            int(self.URL, 16)
            return 1
        except ValueError:
            return 0

    def checkForDigitsInDomain(self):
        for c in self.URL:
            if c.isdigit():
                return 1
        return 0

    def checkAlexaTop1Million(self):
        ext = tldextract.extract(self.host)
        url = ext.domain + '.' + ext.suffix
        if url in alexaSet:
            return 1
        return 0

    def checkSubDomains(self):
        ext = tldextract.extract(self.host)
        sub_domains = ext.subdomain.split('.')
        # numBrandNames = 0
        for sub in sub_domains:
            if sub in alexaNameSet:
                # numBrandNames = numBrandNames + 1
                return 1
        # return numBrandNames
        return 0

    def checkForPunycode(self):
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
