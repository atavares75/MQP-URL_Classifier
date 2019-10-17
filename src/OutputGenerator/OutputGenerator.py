import os

import joblib
import pandas as pd
from OutputGenerator import output_path
import seaborn as sns
import matplotlib.pyplot as plt

class OutputGenerator:

    def __init__(self, model, testing_set, path, metric):
        """
        The initializes the varibles in the OutputGenerator class
        :PARAM trainTest: the TrainTest object
        :PARAM algorithmPerformance: the AlgorithmPerformance object
        """
        self.model = model
        self.testing_set = testing_set
        self.path = output_path + path
        self.metric = metric
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def print_samples(self, tpos_path, tneg_path, fpos_path, fneg_path, label):
        """
        Outputs false positives and negatives and true positives and negatves to separate files
        :PARAM tpos_path: the file path for the true positives
        :PARAM tneg_path: the file path for the true negatives
        :PARAM fpos_path: the file path for the false positives
        :PARAM fneg_path: the file path for the false negatives
        :PARAM label: the category wanted for false positives and negatives
        """
        true_pos_file = open("%s/%s_true_positives.txt" % (tpos_path, label), "w")
        true_pos_file.write("Correct Label: URL\n")

        true_neg_file = open("%s/%s_true_negatives.txt" % (tneg_path, label), "w")
        true_neg_file.write("Correct Label: URL\n")

        false_pos_file = open("%s/%s_false_positives.txt" % (fpos_path, label), "w")
        false_pos_file.write("Correct Label: URL\n")

        false_neg_file = open("%s/%s_false_negatives.txt" % (fneg_path, label), "w")
        false_neg_file.write("Incorrect Label: URL\n")

        correct = self.testing_set.labels
        prediction = self.model.performance.prediction
        test_urls = self.testing_set.urls

        for i in range(len(correct)):
            if correct[i] != label:
                if prediction[i] == label:
                    false_pos_file.write(correct[i] + ": " + str(test_urls[i].encode()) + "\n")
                else:
                    true_neg_file.write(correct[i] + ": " + str(test_urls[i].encode()) + "\n")
            else:
                if prediction[i] != label:
                    false_neg_file.write(prediction[i] + ": " + str(test_urls[i].encode()) + "\n")
                else:
                    true_pos_file.write(correct[i] + ": " + str(test_urls[i].encode()) + "\n")

        true_pos_file.close()
        true_neg_file.close()
        false_pos_file.close()
        false_neg_file.close()

    def print_all(self, path):
        """
        Prints all output to a txt file, saves the ROC graph as a PNG, and saves the model
		"""

        # Print Metrics to output file
        file = open("%s/metric_report.txt" % path, "w")

        file.write("Output for: " + self.model.name + "\n")
        file.write("\nTime to train: ")
        file.write(str(self.model.train_time))
        file.write("\nTime to test: ")
        file.write(str(self.model.test_time))
        file.write("\n\nConfusion Matrix:\n")
        file.write(self.model.performance.cmtx.to_string())
        file.write("\n\nClassification Report:\n")
        file.write(self.model.performance.createClassificationReport())
        file.write("\n\nAccuracy: " + str(self.model.performance.calculateAccuracy()))
        file.write("\n\nFalse Positive Rates:\n")
        file.write(str(self.model.performance.calculateFalsePostiveRate()))
        file.write("\n\nFalse Negative Rates:\n")
        file.write(str(self.model.performance.calculateFalseNegativeRate()))

        file.close()

        # Save ROC graph to file
        fig = self.model.performance.generateROC()
        fig.savefig('%s/ROC_Graph.png' % path, bbox_inches='tight')
        plt.close()

        # Save samples of false positives and negatives and true positives and negatives
        categories = ['Normal', 'phish', 'malware', 'ransomware', 'BotnetC&C']

        tpos_path = "%s/true_positives" % path
        os.mkdir(tpos_path)

        tneg_path = "%s/true_negatives" % path
        os.mkdir(tneg_path)

        fpos_path = "%s/false_positives" % path
        os.mkdir(fpos_path)

        fneg_path = "%s/false_negatives" % path
        os.mkdir(fneg_path)

        for category in categories:
            self.print_samples(tpos_path, tneg_path, fpos_path, fneg_path, category)

    def print_algorithm_performance(self):
        file = open("%s/%s.txt" % (self.path, self.metric), "a")
        file.write("Algorithm name: " + self.model.name)
        file.write("\nParameter values are: " + str(self.model.parameters))
        file.write("\nRun ID: " + str(self.model.id) + "\n")
        file.write(self.metric + ":\n" + str(self.model.performance.get_results(self.metric)))
        file.write("\n\n")
        file.close()
        path = "%s/%s_%s_Output" % (self.path, self.model.id, self.model.name)
        os.mkdir(path)
        # Save model
        joblib.dump(self.model.algorithm, '%s/model.joblib' % path)
        self.print_all(path)

    def print_2d_optimized_output(self, tuning_params, i, j):

        file = open("%s/Optimized_Results.txt" % self.path, "a")
        file.write("Parameter values are: " + tuning_params[0] + ": " + str(i) + " and " + tuning_params[
            1] + ": " + str(j) + "\n")
        file.write("Run ID: " + str(self.model.id) + "\n")
        file.write(self.metric + "\n" + str(self.model.performance.get_results(self.metric)))
        file.write("\n\n")
        file.close()
        path = "%s/%s_%s_%s_Output" % (self.path, self.model.name, str(i), str(j))
        os.mkdir(path)
        self.print_all(path)

    def print_1d_optimized_output(self, i):
        file = open("%s/Optimized_Results.txt" % self.path, "a")
        file.write("Parameter value is " + str(i) + "\n")
        file.write("Run ID: " + str(self.model.id) + "\n")
        file.write(self.metric + "\n" + str(self.model.performance.get_results(self.metric)))
        file.write("\n\n")
        file.close()
        path = "%s/%s_%s_Output" % (self.path, self.model.name, str(i))
        os.mkdir(path)
        self.print_all(path)

    def print_optimized_parameters(self, best):
        file = open("%s/Optimized_Results.txt" % self.path, "a")
        file.write("Best parameter value is " + str(best[1]) + "\n")
        file.write("Run ID: " + str(best[0].id) + "\n")
        file.write(self.metric + "\n" + str(best[0].performance.get_results(self.metric)))
        file.write("\n\n")
        file.close()
        # Save model
        joblib.dump(best[0].algorithm, '%s/optimized_model.joblib' % self.path)

    def print_2d_visual(self, df):
        c = df.columns
        h = df.pivot(c[0], c[1], c[2])
        plt.clf()
        sns.heatmap(h, cmap="YlGnBu")
        fig = plt.gcf()
        fig.savefig('%s/HeatMap.png' % self.path, bbox_inches='tight')
        plt.close()
        df.to_csv("%s/optimize_results.csv" % self.path)

    def print_1d_visual(self, df, tuning_param):
        """
        Prints line chart of metric vs tuning parameter
        :param df: df containing optimization values
        :param tuning_param: the name of the tuning parameter
        """
        axis = {
            "accuracy": "Accuracy (%)",
            "false_positive": "False Positive Rate (%)",
            "false_negative": "False Negative Rate (%)"
        }
        plt.clf()
        sns.set(style='darkgrid')
        sns.lineplot(x=tuning_param, y=axis[self.metric], data=df)
        fig = plt.gcf()
        fig.savefig('%s/OptimizationLineGraph.png' % self.path, bbox_inches='tight')
        plt.close()
        df.to_csv("%s/optimize_results.csv" % self.path)

    def print_probability_output(self, tags):
        """
        Prints output for tagging algorithm
        :param tags: an array of tags
        :return: none
        """
        predictions = list()
        rows, columns = tags.shape
        false_positives = 0
        false_negatives = 0
        for row in range(rows):
            truth = self.testing_set.labels[row]
            prediction_added = False
            temp_prediction = None
            false_reading_added = False
            for column in range(columns):
                if truth == tags[row][column]:
                    prediction_added = True
                    temp_prediction = tags[row][column]
                elif prediction_added == False and tags[row][column] in self.model.algorithm.classes_:
                    prediction_added = True
                    temp_prediction = tags[row][column]
                if(false_reading_added is False):
                    if truth == "Normal" and tags[row][column] != 0 and tags[row][column] != "Normal":
                        false_reading_added = True
                        false_positives += 1
                    if truth != "Normal" and tags[row][column] != 0 and tags[row][column] == "Normal":
                        false_reading_added = True
                        false_negatives += 1
            if prediction_added == False:
                predictions.append('Normal')
            else:
                predictions.append(temp_prediction)
        t = pd.DataFrame(tags)
        labels = pd.DataFrame(self.testing_set.labels)
        df = pd.concat([labels, t], axis=1)
        df.to_csv("%s/tags.csv" % self.path)
        false_file = open("%s/false_tags.txt" % self.path, "w")
        false_file.write("Number of false positives: %i\n" % false_positives)
        false_file.write("Number of false negatives: %i\n" % false_negatives)
        false_file.close()
        self.model.performance.set_prediction(predictions)
        self.model.performance.createConfusionMatrix()
        self.print_algorithm_performance()
