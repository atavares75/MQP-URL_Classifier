


def extractLexicalFeatures(urls):
    features = list()
    i = 0
    for url in urls:
        i = i + 1
        if type(url) is str:
            features.append([len(url), len(url.split('/')[0]), len(url.split('.')) - 1])
        else:
            print(i)
            print(str(url))
    return features
