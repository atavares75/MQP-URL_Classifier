# data_labels = ['Normal', 'malware', 'phish', 'ransomware', 'BotnetC&C']


def convertData(category, labeledData):
    newData = list()
    for entry in labeledData:
        if entry == category:
            newData.append(category)
        else:
            newData.append('Other')
    return newData

