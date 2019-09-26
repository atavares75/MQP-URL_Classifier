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

    def print_false_pos_and_neg(self, pos_path, neg_path, label):
        """
        Outputs fasle positives and negatives to separate files
        :PARAM pos_path: the file path for the false positives
        :PARAM neg_path: the file path fot the false negatives
        :PARAM label: the category wanted for false positives and negatives
        """
        pos_file = open("%s/%s_false_positives.txt" % (pos_path, label), "w")
        pos_file.write("Correct Label: URL\n")

        neg_file = open("%s/%s_false_negatives.txt" % (neg_path, label), "w")
        neg_file.write("Incorrect Label: URL\n")

        correct = self.testing_set.labels
        prediction = self.model.prediction
        test_urls = self.testing_set.urls

        for i in range(len(correct)):
            if correct[i] != label:
                if prediction[i] == label:
                    pos_file.write(correct[i] + ": " + str(test_urls[i]) + "\n")
            else:
                if prediction[i] != label:
                    neg_file.write(prediction[i] + ": " + str(test_urls[i]) + "\n")

        pos_file.close()
        neg_file.close()

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

        # Save false positives
        categories = ['Normal', 'phish', 'malware', 'ransomware', 'BotnetC&C']

        pos_path = "%s/false_positives" % path
        os.mkdir(pos_path)

        neg_path = "%s/false_negatives" % path
        os.mkdir(neg_path)

        for category in categories:
            self.print_false_pos_and_neg(pos_path, neg_path, category)

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
        self.print_all()
