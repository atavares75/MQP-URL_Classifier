

def convertData(category, labelTrain, labelTest):
    newTrain = list()
    newTest = list()
    for entry in labelTrain:
        if entry == category:
            newTrain = category
        else:
            newTrain = 'Other'
    for entry in labelTest:
        if entry == category:
            newTest = category
        else:
            newTest = 'Other'

    labelTrain = newTrain
    labelTest = newTest
