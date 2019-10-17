# metric_report.txt

The metric_report.txt file is created for each model and contains different metrics for the run.

# Example Metric Report
```txt
Output for: RandomForest  

Time to train: 0:00:09.939674  
Time to test: 0:00:00.456087  

Confusion Matrix:  
                  pred: BotnetC&C  pred: Normal  pred: malware  pred: phish  pred: ransomware
true: BotnetC&C               723            10             39           25                 0
true: Normal                   13         13211            146          158                 0
true: malware                   4            49           2065          131                 0
true: phish                    15           118            265         1851                 0
true: ransomware                2             0              0            2               495

Classification Report:  
              precision    recall  f1-score   support

   BotnetC&C       0.96      0.91      0.93       797
      Normal       0.99      0.98      0.98     13528
     malware       0.82      0.92      0.87      2249
       phish       0.85      0.82      0.84      2249
  ransomware       1.00      0.99      1.00       499

    accuracy                           0.95     19322
   macro avg       0.92      0.92      0.92     19322
weighted avg       0.95      0.95      0.95     19322


Accuracy: 0.9494358762032916  

False Positive Rates:  
pred: BotnetC&C    -0.036055
pred: Normal       -0.221250
pred: malware      -0.853890
pred: phish        -0.478064
pred: ransomware   -0.000000
dtype: float64

False Negative Rates:  
true: BotnetC&C     0.092848
true: Normal        0.023433
true: malware       0.081814
true: phish         0.176968
true: ransomware    0.008016
dtype: float64
```

# Description of Output

The "Time to train" value is the time the model took to train on the training data.  
The "Time to test" value is the time the model took to test on the test data.  
The "Confusion Matrix" shows the number of URLs predicted in each category and which redictions were correct.  
The "Classification Report" shows the precision, recall, f1-score, and support for each class and the micro and weighted averages.  
The "Accuracy" is the average accuracy of the model.  
The "False Positive Rates" are the rates for false positives for each class.  
The "False Negative Rates" are the rates for the false negatives for each class.  
