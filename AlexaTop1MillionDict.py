import pandas


d = pandas.read_csv('data/top-1m.csv', sep=',', header=None, names=['Domain'], index_col=0)
alexaDict = d.to_dict('list')
listOfDomains = list(alexaDict.values())
alexaSet = set(listOfDomains[0])

alexaNameSet = set()
for name in alexaSet:
    tokens = name.partition('.')
    alexaNameSet.add(tokens[0])

