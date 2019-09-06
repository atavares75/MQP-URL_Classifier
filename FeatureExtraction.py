import csv
import math
import re
from collections import Counter
from urllib.parse import urlparse

import pandas as pd
import tldextract
import idna
from AlexaTop1MillionDict import alexaSet, alexaNameSet


def extractLexicalFeatures(url_list):
    features = list()
    i = 0
    for url in url_list:
        i = i + 1
        data_point = list()
        if type(url) is str:
            data_point.append(checkLength(url))
            data_point.append(countCharacterInString('.', url))
            data_point.append(countCharacterInString('@', url))
            url = checkURLScheme(url)
            parseResults = urlparse(url)
            data_point.append(checkForParams(parseResults))
            data_point.append(checkForQueries(parseResults))
            data_point.append(checkForFragments(parseResults))
            data_point.append(calculateEntropyOfDomainName(parseResults.netloc))
            data_point.append(checkNonStandardPort(parseResults.netloc))
            data_point.append(checkAlexaTop1Million(parseResults.netloc))
            data_point.append(checkForPunycode(parseResults.netloc))
            data_point.append(checkSubDomains(parseResults.netloc))
            path = parseResults.path
            host = parseResults.netloc
            checkHostName(host, data_point)
            checkPath(path, data_point)
        else:
            print(i)
            print(str(url))
        features.append(data_point)
    return features


def checkHostName(host, features):
    # '-' in host
    features.append(checkForCharacter('-', host))
    # digits in host
    features.append(checkForDigits(host))
    # length of host
    features.append(checkLength(host))
    # number of '.' in host
    features.append(countCharacterInString('.', host))
    # IP based host
    features.append(checkForIPAddress(host))  # optimal
    # Hex based host
    features.append(checkHexBasedHost(host))
    # Is TLD common
    features.append(checkTLD(host))


def checkPath(path, features):
    features.append(countCharacterInString('-', path))  # optimal
    features.append(countCharacterInString('/', path))  # 15
    features.append(countCharacterInString('=', path))
    features.append(countCharacterInString(';', path))
    features.append(countCharacterInString(',', path))
    features.append(countCharacterInString('-', path))
    features.append(countCharacterInString('.', path))
    features.append(checkLength(path))
    # features.append(countCharacterInString('?', path)) # optimal
    features.append(countCharacterInString('&', path))
    features.append(checkForUsernameOrPassword(path))


def checkURLScheme(url):
    tokens = url.partition('://')
    if len(tokens[1]) == 0:
        # no protocol in front of url
        return '//' + url
    else:
        return url


def checkForCharacter(character, string):
    return 1 if character in string else 0


def countCharacterInString(character, string):
    return sum(map(lambda x: 1 if character in x else 0, string))


def checkLength(url):
    return len(url)


def checkNonStandardPort(netloc):
    port = netloc.rpartition(':')[2]
    standardPorts = ['80', '443', '8080']
    if len(port) > 0 and port.isdigit():
        if port in standardPorts:
            return 0
        else:
            return 1
    else:
        return 0


def checkForFragments(parsed_url):
    return 1 if len(parsed_url.fragment) > 0 else 0


def checkForQueries(parsed_url):
    return 1 if len(parsed_url.query) > 0 else 0


def checkForParams(parsed_url):
    return 1 if len(parsed_url.params) > 0 else 0


def checkTLD(hostname):
    popularTLDs = ['com', 'net', 'gov', 'edu', 'org', 'de']
    ext = tldextract.extract(hostname)
    return 0 if ext.domain in popularTLDs else 1


def checkForIPAddress(url):
    regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', url)
    return 1 if regex is not None else 0


def checkForUsernameOrPassword(path):
    lowerPath = path.lower()
    i = 0
    if 'username' in lowerPath:
        i = i + 1
    if 'password' in lowerPath:
        i = i + 1
    return i


def calculateEntropyOfDomainName(host):
    p, lengths = Counter(host), float(len(host))
    return -sum(count / lengths * math.log2(count / lengths) for count in p.values())


def checkHexBasedHost(url):
    try:
        int(url, 16)
        return True
    except ValueError:
        return False


def checkForDigits(url):
    for c in url:
        if c.isdigit():
            return 1
    return 0


def checkAlexaTop1Million(host_name):
    ext = tldextract.extract(host_name)
    url = ext.domain + '.' + ext.suffix
    if url in alexaSet:
        return 1
    return 0


def checkSubDomains(host_name):
    ext = tldextract.extract(host_name)
    sub_domains = ext.subdomain.split('.')
    for sub in sub_domains:
        if sub in alexaNameSet:
            return 1
    return 0


def checkForPunycode(host):
    for c in host:
        if not c.isascii():
            print('Non ASCII: ' + host)
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
