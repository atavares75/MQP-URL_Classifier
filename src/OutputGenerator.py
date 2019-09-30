# Robert Dwan 

import os, joblib
import numpy as np

class OutputGenerator:

    def __init__(self, model, testing_set, path):
        """
        The initializes the varibles in the OutputGenerator class
        :PARAM trainTest: the TrainTest object
        :PARAM algorithmPerformance: the AlgorithmPerformance object
        """
        self.model = model
        self.testing_set = testing_set
        self.path = path

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
        prediction = self.model.prediction
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

    def print_all(self):
        """
        Prints all output to a txt file, saves the ROC graph as a PNG, and saves the model
		"""
        path = "%s/%s_%s_Output" % (self.path, self.model.id, self.model.name)
        os.mkdir(path)

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

        # Save model
        joblib.dump(self.model.algorithm, '%s/model.joblib' % path)

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

    def print_probability_output(self, tags):
        predictions = np.zeros(shape=(self.testing_set.labels.shape), dtype=object)
        rows, columns = tags.shape
        for row in range(rows):
            truth = self.testing_set.labels[row]
            prediction_correct = False
            for column in range(columns):
                if truth == tags[row][column]:
                    prediction_correct = True
                    predictions[row] = tags[row][column]
                elif prediction_correct == False and tags[row][column] in self.model.algorithm.classes_:
                    predictions[row] = tags[row][column]
            if predictions[row] == 0:
                predictions[row] = 'Normal'
        self.model.performance.set_prediction(predictions)
        self.model.performance.createConfusionMatrix()
        self.print_all()
