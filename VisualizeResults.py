import seaborn
import matplotlib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
import logging.handlers
import os

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "data/log/results-log.log"))
FORMAT = '%(message)s'
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
results_log = logging.getLogger()
results_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
results_log.addHandler(handler)

handler2 = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "data/log/feature-log.log"))
FORMAT2 = '%(message)s'
formatter2 = logging.Formatter(FORMAT2)
handler2.setFormatter(formatter2)
feature_log = logging.getLogger()
feature_log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
feature_log.addHandler(handler2)

data_labels = ['Normal', 'malware', 'phish', 'ransomware', 'BotnetC&C']


def visualize(label_test, prediction):
    c_matrix = confusion_matrix(label_test, prediction, data_labels)
    classif_report = classification_report(label_test, prediction)
    accuracy = accuracy_score(label_test, prediction)
    results_log.info(c_matrix)
    results_log.info(classif_report)
    results_log.info(accuracy)
    results_log.info('\n')


def evaluateFeatures(eval_algorithm, training_features, training_output):
    algo = evaluation_algorithm(eval_algorithm)
    selector = RFECV(algo, step=1, cv=5)
    selector = selector.fit(training_features, training_output)
    e = selector.support_
    f = selector.score(training_features, training_output)
    feature_log.info(e)
    feature_log.info(f)
    feature_log.info('\n')


def evaluation_algorithm(input_algorithm):
    switcher = {
        "rf": RandomForestClassifier(n_estimators=25, max_depth=None, max_features=0.4, random_state=11),
        "lr": LogisticRegression(multi_class='multinomial', solver='lbfgs'),
        "svm-l": LinearSVC(dual=False, fit_intercept=False, max_iter=1700, C=1),
        "svm-rbf": SVC(kernel='rbf', gamma='auto', max_iter=100000, C=1)
    }
    return switcher.get(input_algorithm, lambda: "Invalid Algorithm")
