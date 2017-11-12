#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

import pprint
import numpy as np
import  matplotlib.pyplot as pyplot
from tester import test_classifier
from tester import dump_classifier_and_data
from feature_format import featureFormat, targetFeatureSplit


#########################################################################
### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
##########################################################################
features_list = ['poi',
				'other',
				'expenses', 
				'exercised_stock_options',
				'from_this_person_to_poi_rate',
				'exercised_stock_options_value_rate']
				# You will need to use more features
########################################################################
###
### Load the dictionary containing the dataset
###
########################################################################
with open("final_project_dataset.pkl", "r") as data_file:
	data_dict = pickle.load(data_file)

########################################################################
### Datasets and Questions
########################################################################

### total number of data points
names = data_dict.keys()
print("Total number of data points:{}".format(len(names)))

### allocation across classes(POI/non-POI)
POIs = [data_dict[name]['poi'] for name in names if data_dict[name]['poi']==True]
print('POI numbers:%r'%(len(POIs)))
non_POIs = [data_dict[name]['poi'] for name in names if data_dict[name]['poi']==False]
print('non-POIs numbers:{}'.format(len(non_POIs)))

########################################################################
### Task 2: Remove outliers
########################################################################

### number of features used

number_features = len(data_dict['TOTAL'])
print("Number of features used:%s"%(number_features))

### Number of missed values in features

keys = data_dict['TOTAL'].keys()
F_missed = [key for name in names for key in keys if data_dict[name][key]=='NaN']
F_number = [(key,F_missed.count(key))for key in keys if key in F_missed]

many_missed_fvalues = []
for row in F_number:
	if row[1]:
		many_missed_fvalues.append(row)
print("The number of Missed feature's values:")
pprint.pprint(many_missed_fvalues)


# get the outliers information
def get_outliers_names(data_dict, field1, field2):
	outliers_names = []
	for name in names:
		people = data_dict[name]
		value1 = people[field1]
		value2 = people[field2]
		if (people[field1]!='NaN')and(people[field2]!='NaN'):
			if (value2>3.0*pow(10,8))or(abs(value1)>3*pow(10,8)):
				outliers_names.append(name)
	return outliers_names

outliers_names = get_outliers_names(data_dict,'exercised_stock_options','total_stock_value')

for name in names:
	# check the name not match the special format.
	namelist = name.split()
	if len(namelist) > 4:
		outliers_names.append(name)
	# check the person only have one type value.
	people = data_dict[name]
	coll = set(people.values())
	if len(coll)<=2:
		outliers_names.append(name)

# remove the outliers and get new dataset
def sub_dict(somedict, somekeys, default=None):
	return dict([(k, somedict.get(k, default)) for k in somekeys if k not in outliers_names])

def sub_outliers(somedict, somekeys, default=None):
	return dict([(k, somedict.get(k, default))for k in somekeys if k in outliers_names]) 

outliers = sub_outliers(somedict=data_dict, somekeys=names)
my_data_dict = sub_dict(somedict=data_dict, somekeys=names)

#########################################################################################
###
### Task 3: Create new feature(s).Store to my_dataset for easy export below.
###
#########################################################################################

# extract the column values

def get_elements(value):
	x = []
	for name in my_data_dict.keys():
		people = my_data_dict[name]
		if people[value]=='NaN':
			people[value] = 0.0
		x.append(people[value])
	x = np.array(x)
	return x

to_messages = get_elements("to_messages")
from_messages = get_elements("from_messages")
from_poi_to_this_person = get_elements('from_poi_to_this_person')
from_this_person_to_poi = get_elements('from_this_person_to_poi')
exercised_stock_options = get_elements('exercised_stock_options')
total_stock_value = get_elements('total_stock_value')

# get the friction of two columns
def get_friction(numpy1,numpy2):
	results = []
	for n in range(len(numpy1)):
		if (numpy1[n]==0.0)or(numpy2[n]==0.0):
			result = 0.0
		else:
			result = numpy1[n]/numpy2[n]
		results.append(result)
	return results

from_this_person_to_poi_rate = get_friction(from_this_person_to_poi, from_messages)
from_poi_to_this_person_rate = get_friction(from_poi_to_this_person, to_messages)
exercised_stock_options_value_rate = get_friction(exercised_stock_options, total_stock_value)

keys = my_data_dict.keys()

for n in range(len(keys)):
	key = keys[n]
	people = my_data_dict[key]
	# add value to people's dictionary
	people['from_this_person_to_poi_rate'] = from_this_person_to_poi_rate[n]
	people['from_poi_to_this_person_rate'] = from_poi_to_this_person[n]
	people['exercised_stock_options_value_rate'] = exercised_stock_options_value_rate[n]
	my_data_dict[key] = people

my_dataset = my_data_dict
data = featureFormat(my_dataset, features_list, sort_keys = True)

# Extract features and labels from dataset for local testing
labels, features = targetFeatureSplit(data)

#######################################################
###
###  Preprocessing the data
###
#######################################################

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif

### Use the Standard Feature Scaling 

scaler = preprocessing.MinMaxScaler()
scaled_features = scaler.fit_transform(features)
print("Feature Scaling\n")
print(scaled_features.shape)

### Select feature
select = SelectKBest(f_classif, k="all")
selecter = select.fit(scaled_features, labels)
selected_features = selecter.transform(scaled_features)

select_score = selecter.scores_
print("SelectKBest Feature  Scores:\n")
pprint.pprint(dict(zip(features_list[1:], select_score)))

######################################################################
### Split training and test dataset
test_size = 0.3
random_state = 46

features_train, features_test, labels_train, labels_test = \
	train_test_split(selected_features, labels, test_size=test_size, random_state=random_state)

###################################################################
### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html
###################################################################

# Provided to give you a starting point. Try a variety of classifiers.

### Import different classifiers 
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# Evaluate the  Classifier's performance
def test_evaluation(clf):
	labels_pred = clf.predict(features_test)
	print("Classifier :\n{}".format(str(clf)))

	# Accuracy Score
	accu_score = accuracy_score(labels_test, labels_pred)
	print("Accuracy Score:{}\n".format(accu_score))
	

	# Precision Score
	prec = precision_score(labels_test, labels_pred)
	print("Precision Score: {}\n".format(prec))

	# Recall Score
	recall = recall_score(labels_test, labels_pred)
	print("Recall Score: {}\n".format(recall))
	
	# Classification Report
	class_report = classification_report(labels_test, labels_pred)
	print("classification_Report:\n{}".format(class_report))

	# Confusion Matrix
	con_matrix = confusion_matrix(labels_test, labels_pred)
	print("Confusion Matrix:\n{}".format(con_matrix))
			

# LogisticRegression
ls = LogisticRegression().fit(features_train, labels_train)
print(ls.score(features_test, labels_test))

# Support Vector Machine
SVM = SVC(kernel='linear').fit(features_train, labels_train)
test_evaluation(SVM)

# DecisionTree Classifier
dt = DecisionTreeClassifier(max_depth=5)
dt1= dt.fit(features_train, labels_train)
test_evaluation(dt1)
# print the DecisionTreeClassifier's Feature Importances 
print("DecisionTree:\n{}".format(dt1.feature_importances_))

# RandomForestClassifier
rfc = RandomForestClassifier(max_depth=5, n_estimators=10, max_features=None, warm_start=True)
rfc_1 = rfc.fit(features_train,labels_train)
# Evaluate the classifier's precison, recall and f1-score
test_evaluation(rfc_1)
# print out The importances of the RandomForestClassifier's features
print("RandomForestClassifier Feature Importance:\n")
print(rfc_1.feature_importances_)


# Naive Bayes
gnb = GaussianNB().fit(features_train, labels_train)
test_evaluation(gnb)

# AdaBoostClassifier
abc = AdaBoostClassifier().fit(features_train, labels_train)
test_evaluation(abc)
print("AdaBoostClassifier Features Importance:\n{}".format(abc.feature_importances_))

# KNN 
KNN = KNeighborsClassifier(n_neighbors=3)
knn = KNN.fit(features_train, labels_train)
from sklearn.model_selection import cross_val_score
print("KNN Cross_Val_Score")
print(cross_val_score(knn, features_train, labels_train, cv=4))


#################################################################################
### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
###################################################################################

# Example starting point. Try investigating other evaluation techniques!

# Import GridSearchCV
from time import time 
from tester import test_classifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit

cv = StratifiedShuffleSplit(n_splits=10, test_size=test_size, random_state=random_state)

# prepare a range of estimator values to test
para_estims = np.arange(10, 100, 10)

# Set the parameter candidates
param_grid = [
				{'algorithm':['SAMME'],'n_estimators':para_estims},
				{'algorithm':['SAMME','SAMME.R']},
				{'algorithm':['SAMME.R'],'n_estimators':para_estims}
				]

# Create a classifier with the parameter candidates
model = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),random_state=random_state)

grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv)

# Train the classifier on training data
grid = grid.fit(features_train, labels_train)

# summarize the results of the grid search
print(grid.best_score_)

clf = grid.best_estimator_.fit(features_train, labels_train)

test_evaluation(clf)

cross_v_score = cross_val_score(clf, features_test, labels_test)

print("Cross_Val_Score:\n{}".format(cross_v_score))

clf = grid.best_estimator_

##########################################################################################
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.
###########################################################################################

dump_classifier_and_data(clf, my_dataset, features_list)

print("Test Classifier:\n")

t0 = time()

test_classifier(clf, my_dataset, features_list)

print("Time:{}".format(round(time()-t0, 3)))
