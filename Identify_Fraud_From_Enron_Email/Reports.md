
# Goal and methods

## goal

  Use the dataset of my selected features to create and tuning relevant parameters 
to optimize my model. 

## methods
  When I watch the < Enron, the smartest boy in the room >,I found the mainly data were disposed after
the scandal exposed. And The goverment workers, the company's internal person and the Accounting Firm 
formming a steady triangular profit. As the consequence, there exist many missed values.
  My model is AdaBoostClassifier.At first,I list all the features when I have no idea which feature may
impact the performance.At the meantime,I add some new features that may influence the output in my thoughts.Testing different classifiers and observing their elaluation and validation resluts.Then Choose my own algorithm.Transform the features's dimension according to the importance of the classifier's features.Thirdly,my features and dataset are splitted again.Change the n_estimator's value with different algorithm to optimize my model.At this section,We might need to test different number of features to ensure the tester's precision and recall score all over 0.3.

## Outliers
  When processing the outlier investigation, We found there are several data points are appeartly 
different from the major points.When print out those abnormal points,It retains the POI and a person named "TOTAL".The "TOTAL" isn't a man's name information and it could be the statistics information.
So this point should be removed and the others are better be reserved.

### The total number of data points : 146

### POI Numbers : 18

## non-POIs Number : 128

# Identify POI's Features

## Selected Features
  By observing the results from my optimized model,The selected features are changeble as the random 
state is't None. The first feature 'other' is always in the selected features.We could found the result
inclined there exist many other factors we haven't discovered.Because the Feature scaling doesn't influence a decision tree algorithm, we choose scale the features to simplify the amount of calculation. 

### SelectKBest Feature Scores
```python
SelectKBest Feature Scores:
{
 'exercised_stock_options_value_rate': 0.26274633267621161,
 'from_this_person_to_poi_rate': 14.790896748252729,
 'exercised_stock_options': 22.840928040757298,
 'expenses': 5.1259732738974915,
 'other': 3.7788629620162775
 }
```

### Select features manually

#### The first all features are selected,The Algorithm Feature Importances
```python
('other', 0.21202)
('bonus', 0.0)
('salary', 0.0)
('expenses', 0.17786)
('to_messages', 0.0)
('loan_advances', 0.0)
('from_messages', 0.07538)
('director_fees', 0.0)
('total_payments', 0.0)
('deferred_income', 0.0)
('restricted_stock', 0.10081)
('deferral_payments', 0.0)
('total_stock_value', 0.18057)
('long_term_incentive', 0.0)
('shared_receipt_with_poi', 0.0)
('exercised_stock_options', 0.0)
('from_this_person_to_poi', 0.0)
('from_poi_to_this_person', 0.0)
('restricted_stock_deferred', 0.0)
('from_this_person_to_poi_rate', 0.25335)
('from_poi_to_this_person_rate', 0.0)
('exercised_stock_options_value_rate', 0.0)

Precison Score : 0.0
Recall Score : 0.0
```

####  The second time I tried removing some features which have zero-importance in the algorithm.The result is amazing.Though the algorithm fitted new-selected features doesn't well in the testing dataset, It has a good performance in the final tester.
```python
('other', 0.25)
('expenses', 0.14999999999999999)
('to_messages', 0.0)
('from_messages', 0.050000000000000003)
('restricted_stock', 0.14999999999999999)
('total_stock_value', 0.10000000000000001)
('long_term_incentive', 0.0)
('shared_receipt_with_poi', 0.0)
('exercised_stock_options', 0.14999999999999999)
('from_this_person_to_poi', 0.050000000000000003)
('from_poi_to_this_person', 0.0)
('restricted_stock_deferred', 0.0)
('from_this_person_to_poi_rate', 0.10000000000000001)
('from_poi_to_this_person_rate', 0.0)
('exercised_stock_options_value_rate', 0.0)

Precision Score: 0.285714285714
Recall Score: 0.5
```

####  The third time to remove some zero-importance features
```python
('other', 0.26666666666666666)
('expenses', 0.13333333333333333)
('from_messages', 0.066666666666666666)
('restricted_stock', 0.13333333333333333)
('total_stock_value', 0.10000000000000001)
('exercised_stock_options', 0.13333333333333333)
('from_this_person_to_poi', 0.066666666666666666)
('from_poi_to_this_person', 0.0)
('restricted_stock_deferred', 0.0)
('from_this_person_to_poi_rate', 0.10000000000000001)
('from_poi_to_this_person_rate', 0.0)
('exercised_stock_options_value_rate', 0.0)

Precision Score: 0.142857142857
Recall Score: 0.25
Accuracy Score: 0.790697674419
Confusion_Matrix:
[[33  6]
 [ 3  1]]
Test Classifier:

AdaBoostClassifier(algorithm='SAMME.R',
          base_estimator=DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=1,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'),
          learning_rate=1.0, n_estimators=30, random_state=46)
  Accuracy: 0.86660 Precision: 0.49970  Recall: 0.41650 F1: 0.45432 F2: 0.43085
  Total predictions: 15000  True positives:  833  False positives:  834 False negatives: 1167 True negatives: 12166

Time:71.646
```

#### Continue to remove some zero-importance features 
```python
('other', 0.24285714285714285)
('expenses', 0.15714285714285714)
('from_messages', 0.085714285714285715)
('restricted_stock', 0.11428571428571428)
('total_stock_value', 0.15714285714285714)
('exercised_stock_options', 0.085714285714285715)
('from_this_person_to_poi', 0.057142857142857141)
('from_this_person_to_poi_rate', 0.085714285714285715)
('exercised_stock_options_value_rate', 0.014285714285714285)

Precision Score: 0.5
Recall Score: 0.75
Accuracy Score: 0.906976744186

Confusion_Matrix:
[[36  3]
 [ 1  3]]
Test Classifier:

AdaBoostClassifier(algorithm='SAMME.R',
          base_estimator=DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=1,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'),
          learning_rate=1.0, n_estimators=70, random_state=46)
  Accuracy: 0.85973 Precision: 0.46570  Recall: 0.35300 F1: 0.40159 F2: 0.37095
  Total predictions: 15000  True positives:  706  False positives:  810 False negatives: 1294 True negatives: 12190

Time:165.356
```

####  When I delected some zero-importance features, I found the final tester's performance down as the testing's performance is good.I realized it might be overfitting.So I choose some high features and several deleted zero-importance features to test.
```python
features_list = ['poi', 'other','expenses', 'from_this_person_to_poi_rate', 'exercised_stock_options_value_rate', 'exercised_stock_options']

Accuracy Score: 0.780487804878
Confusion_Matrix:
[[29  3]
 [ 6  3]]

classification_Report:
             precision    recall  f1-score   support

        0.0       0.83      0.91      0.87        32
        1.0       0.50      0.33      0.40         9

avg / total       0.76      0.78      0.76        41

Precision Score: 0.5
Recall Score: 0.333333333333

Test Classifier:

AdaBoostClassifier(algorithm='SAMME',
          base_estimator=DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=1,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'),
          learning_rate=1.0, n_estimators=40, random_state=46)
  Accuracy: 0.87279 Precision: 0.57567  Recall: 0.41650 F1: 0.48332 F2: 0.44088
  Total predictions: 14000  True positives:  833  False positives:  614 False negatives: 1167 True negatives: 11386

Time:88.243
```
####  The result validates my suspection.We need some high importance features.We also need some unrelevant features to avoid the model overfitting.
```python
feature_list = ['poi','expenses', 'exercised_stock_options', 'restricted_stock',
        'from_poi_to_this_person_rate', 'from_poi_to_this_person_rate',  'exercised_stock_options_value_rate']
Accuracy Score: 0.857142857143

Confusion_Matrix:
[[36  1]
 [ 5  0]]

classification_Report:
             precision    recall  f1-score   support

        0.0       0.88      0.97      0.92        37
        1.0       0.00      0.00      0.00         5

avg / total       0.77      0.86      0.81        42


Precision Score: 0.0
Recall Score: 0.0

Test Classifier:

AdaBoostClassifier(algorithm='SAMME',
          base_estimator=DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=1,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'),
          learning_rate=1.0, n_estimators=40, random_state=46)
  Accuracy: 0.84893 Precision: 0.45283  Recall: 0.27600 F1: 0.34296 F2: 0.29938
  Total predictions: 14000  True positives:  552  False positives:  667 False negatives: 1448 True negatives: 11333

Time:91.101
```
####  When I test to remove the feature 'other', the algorithm performance doesn't well and the recall score doesn't over 0.3. So,th feature 'other' have a important role in the model.

## Create my own features
  During the documents,We found it mentioned the stock and stock value many times.Before the Enron 
Scandal broken out,the senior management staff of the company frequently sold their owned stock even 
under the condition of the stock value in the trading was high.We also add the new feature in the feature list to test its influence.
  I also test selecting features by hand.The 'other','from_this_person_to_poi_rate','total_stock_value'
and 'exercised_stock_options' has a high precision and recall in predition's score.The different combinations could have different improvement in final teater's procedure.I tried the only two features of 'other' and 'from_this_person_to_poi_rate',the results meet the requirements.Confusing the
results,It might be the serious missed data values.The data we can't figure out its source has a high 
suspection.It's essential to clear the source of money and its way.

# Algorithm

## My choosed Algorithm : AdaBoostClassifier

## Other tested algorithm

### Naive Bayes --- GaussianNB(priors=None)
### Decision Tree : 
	RandomForestClassifier(),
	DecisionTreeClassifier(),
	AdaBoostClassifier()

### Linear Model --- LogisticRegression()

## Tune algorithm 
  At first,The different running time and The 'SAMME.R' run a real boosting algorithm, but the 'SAMME' will use discrete boosting algorithm.Secondly, They have different requirement in base algorithm.The base algorithm of "SAMME.R" must have the capality of calculating the class's probabilities.The 'SAMME.R' run faster and have a lower tester error than "SAMME".

```python
Accuracy Score:0.780487804878
Precision Score: 0.5
Recall Score: 0.333333333333

Test Classifier:

AdaBoostClassifier(algorithm='SAMME',
          base_estimator=DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=1,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'),
          learning_rate=1.0, n_estimators=40, random_state=46)
	Accuracy: 0.87279	Precision: 0.57567	Recall: 0.41650	F1: 0.48332	F2: 0.44088
	Total predictions: 14000	True positives:  833	False positives:  614	False negatives: 1167	True negatives: 11386

Time:94.521
```

# Tune the parameter

## Tuned parameters

### algorithm: Use a real boosting algorithm or use the discrete boosting algorithm.
### algorithm tuned parameters: SAMME, SAMME.R

### n_estimators : The terminated boosting estimators's maximum number.
### estimators tuned parameter:[10,20,30,40,50,60,70,80,90,100]

## What can happened if we don't tune the parameters of a algorithm?
  We could found the different parameter of a algorithm have different preformances.If this section 
doesn't well, we could discover even the same algorithm, the preformance maybe worse with a unsuitble
parameter.

# Validation

## Validation
  Validation is splitting the data into testing and training dataset.

## Validation Importance
  Because it helps ue to test our model whether overfitting and estimate the performance of an independent dataset.  

## Validation Strategy
  Stratified shuffle splitting the data into ten parts. the testing dataset occupies 0.3 to test the model after fitting the training dataset to test the model's prediction.

# Evaluation 

## Classification Report
```python
classification_Report:
                 precision    recall  f1-score   support

        0.0       0.83      0.91      0.87        32
        1.0       0.50      0.33      0.40         9

avg / total     0.76      0.78      0.76        41
Accuracy Score:0.780487804878
Precision Score: 0.5
Recall Score: 0.333333333333
```
### Precison
  Precision is also called positive predictive value.It is the fraction of relevant instances among the retrieved instances. It reflect how many selected items are relevant.
### Recall
  Recall is also called true positive rate.It is percentage of relevant instances that have been retrieved over the total amount of relevant instances.It reflect how many relevant items are selected.

  Given unknown labels dataset,Precison is thetrue  percentage of targets in total POIs that my 
algorithm predicted it as positive. The recall is the target POIs percentage of all forecasts correspond 
with the actual situation.
  In my algorithm's performance,there exist the precision and recall all zero because of its no 
true positive value.


```python

```
