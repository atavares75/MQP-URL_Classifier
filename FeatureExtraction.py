import re


def extractLexicalFeatures(urls):
    features = list()
    i = 0
    for url in urls:
        i = i + 1
        data_point = list()
        if type(url) is str:
            data_point.append(checkLength(url))
            data_point.append(countCharacterInString('.', url))
            data_point.append(countCharacterInString('@', url))
            (protocol, host, path) = tokenizeURL(url)
            data_point.append(len(path))
            checkHostName(host, data_point)
            checkPath(path, data_point)
        else:
            print(i)
            print(str(url))
        features.append(data_point)
    return features


def tokenizeURL(url):
    tokens = url.partition('://')
    if len(tokens[1]) == 0:
        # no protocol in front of url
        protocol = ''
        host_path = tokens[0].partition('/')
    else:
        protocol = tokens[0]
        host_path = tokens[2].partition('/')

    host = host_path[0]
    path = '/' + host_path[2]

    return protocol, host, path


def checkForCharacter(character, string):
    return 1 if character in string else 0


def countCharacterInString(character, string):
    return sum(map(lambda x: 1 if character in x else 0, string))


def checkLength(url):
    return len(url)


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
    features.append(checkForIPAddress(host))
    # Hex based host
    features.append(checkHexBasedHost(host))


def checkPath(path, features):
    features.append(countCharacterInString('-', path))
    features.append(countCharacterInString('/', path))
    features.append(countCharacterInString('=', path))
    features.append(countCharacterInString(';', path))
    features.append(countCharacterInString(',', path))
    features.append(countCharacterInString('-', path))
    features.append(countCharacterInString('.', path))
    features.append(checkLength(path))


def checkForIPAddress(url):
    regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})$', url)
    if regex is not None:
        return 1
    else:
        return 0


def checkHexBasedHost(url):
    try:
        int(url, 16)
        return True
    except ValueError:
        return False


def checkForDigits(url):
    i = 0
    for c in url:
        if c.isdigit():
            i = i + 1
    return i

# extractLexicalFeatures(['www.goog-le.com/about', 'http://amazon.org/yep'])

# tokenizeURL('http://www.goog-le.com/about')
# print(checkForIPAdress('https://www.2345.3453.222.3454.com/about'))
