import seaborn
import matplotlib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def visualize(label_test, prediction):
    print(confusion_matrix(label_test, prediction))
    print(classification_report(label_test, prediction))
    print(accuracy_score(label_test, prediction))


def evaluateFeatures():
    pass