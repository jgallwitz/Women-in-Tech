# -*- coding: utf-8 -*-
"""WIT_DT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1x9IRsRBzIiOanAQo_nJ-QBYTDt_FBXbf
"""

# import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read in CSV file and view dataset
jobs_survey = pd.read_csv('/content/job_survey.csv')
jobs_survey.head()

# dropping all rows that are outside of the US
jobs_survey = jobs_survey.drop(jobs_survey[jobs_survey['Country'] != 'United States of America'].index)

# dropping all NonDev employees
jobs_survey = jobs_survey.drop(jobs_survey[jobs_survey['MainBranch'] != 'Dev'].index)

# drop all nonbinary respondents since I want to compare men and women
jobs_survey = jobs_survey.drop(jobs_survey[jobs_survey['Gender'] == 'NonBinary'].index)

# reindexing
jobs_survey = jobs_survey.reset_index(drop=True)

# turning 'Age' into Boolean
jobs_survey['Age'] = jobs_survey['Age'].replace({'<35': 0})
jobs_survey['Age'] = jobs_survey['Age'].replace({'>35': 1})

# turning 'Accessibility' into Boolean
jobs_survey['Accessibility'] = jobs_survey['Accessibility'].replace({'No': 0})
jobs_survey['Accessibility'] = jobs_survey['Accessibility'].replace({'Yes': 1})

# turning 'MentalHealth' into Boolean
jobs_survey['MentalHealth'] = jobs_survey['MentalHealth'].replace({'No': 0})
jobs_survey['MentalHealth'] = jobs_survey['MentalHealth'].replace({'Yes': 1})

"""DT 1"""

# drop specified columns
jobs_survey_DT = jobs_survey.drop(columns = ['Unnamed: 0','HaveWorkedWith', 'EdLevel', 'MainBranch', 'Country'])

# import libraries for DT
from sklearn.model_selection import train_test_split
from sklearn import tree
import graphviz

# split data up into train and test sets
DT_train, DT_test = train_test_split(jobs_survey_DT, test_size = .3)

# set label for train and test sets
DT_train_label = DT_train["Gender"]
DT_test_label = DT_test["Gender"]

# drop label
DT_train = DT_train.drop(["Gender"], axis=1)
DT_test = DT_test.drop(["Gender"], axis=1)

# execute oversample because women are underrepresented in dataset

# import library
from sklearn.utils import resample

# define majority and minority classes
majority_class = DT_train[DT_train_label == 'Man']
minority_class = DT_train[DT_train_label == 'Woman']

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace=True, n_samples=len(majority_class), random_state=1776)

# combine back to single train set
DT_train = pd.concat([majority_class, minority_upsampled])
DT_train_label = pd.concat([DT_train_label[DT_train_label == 'Man'], DT_train_label[DT_train_label == 'Woman']]).reindex(DT_train.index)

# instantiate decision tree
myTree = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = 2)

# fit DT model
myTree.fit(DT_train, DT_train_label)

# define feature names
FeatureNames = DT_train.columns.values

# define class names
ClassNames = myTree.classes_

# visualize decision tree

# import library
import matplotlib.pyplot as plt

# plot decision tree
plt.figure(figsize = (20, 10))
MyPlot = tree.plot_tree(myTree, feature_names = FeatureNames, class_names = ClassNames)
plt.show()

# create confusion matrix for DT1

# import library
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# use decision tree to make predictions
DT_test_pred = myTree.predict(DT_test)

# build confusion matrix
conf_matrix = confusion_matrix(DT_test_label, DT_test_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = ClassNames)
disp.plot(cmap = 'Blues')
plt.show()

# calculate and print accuracy score

# import library
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(DT_test_label, DT_test_pred)
print(f"Accuracy: {accuracy:.2f}")

"""DT 2"""

# drop specified columns
jobs_survey_DT = jobs_survey.drop(columns = ['Unnamed: 0','HaveWorkedWith', 'EdLevel', 'MainBranch', 'Country', 'MentalHealth'])

# split data up into train and test sets
DT_train, DT_test = train_test_split(jobs_survey_DT, test_size = .3)

# set label for train and test sets
DT_train_label = DT_train["Gender"]
DT_test_label = DT_test["Gender"]

# drop label
DT_train = DT_train.drop(["Gender"], axis=1)
DT_test = DT_test.drop(["Gender"], axis=1)

# execute oversample because women are underrepresented in dataset

# import library
from sklearn.utils import resample

# define majority and minority classes
majority_class = DT_train[DT_train_label == 'Man']
minority_class = DT_train[DT_train_label == 'Woman']

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace=True, n_samples=len(majority_class), random_state=1776)

# combine back to single train set
DT_train = pd.concat([majority_class, minority_upsampled])
DT_train_label = pd.concat([DT_train_label[DT_train_label == 'Man'], DT_train_label[DT_train_label == 'Woman']]).reindex(DT_train.index)

# instantiate decision tree
myTree = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = 2)

# fit DT model
myTree.fit(DT_train, DT_train_label)

# define feature names
FeatureNames = DT_train.columns.values

# define class names
ClassNames = myTree.classes_

# visualize decision tree

# plot decision tree
plt.figure(figsize = (20, 10))
MyPlot = tree.plot_tree(myTree, feature_names = FeatureNames, class_names = ClassNames)
plt.show()

# create confusion matrix

# use decision tree to make predictions
DT_test_pred = myTree.predict(DT_test)

# build confusion matrix
conf_matrix = confusion_matrix(DT_test_label, DT_test_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = ClassNames)
disp.plot(cmap = 'Blues')
plt.show()

# calculate and print accuracy score

accuracy = accuracy_score(DT_test_label, DT_test_pred)
print(f"Accuracy: {accuracy:.2f}")

"""DT3"""

# drop specified columns
jobs_survey_DT = jobs_survey.drop(columns = ['Unnamed: 0','HaveWorkedWith', 'EdLevel', 'MainBranch', 'Country', 'MentalHealth', 'YearsCode'])

# split data up into train and test sets
DT_train, DT_test = train_test_split(jobs_survey_DT, test_size = .3)

# set label for train and test sets
DT_train_label = DT_train["Gender"]
DT_test_label = DT_test["Gender"]

# drop label
DT_train = DT_train.drop(["Gender"], axis=1)
DT_test = DT_test.drop(["Gender"], axis=1)

# execute oversample because women are underrepresented in dataset

# import library
from sklearn.utils import resample

# define majority and minority classes
majority_class = DT_train[DT_train_label == 'Man']
minority_class = DT_train[DT_train_label == 'Woman']

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace=True, n_samples=len(majority_class), random_state=1776)

# combine back to single train set
DT_train = pd.concat([majority_class, minority_upsampled])
DT_train_label = pd.concat([DT_train_label[DT_train_label == 'Man'], DT_train_label[DT_train_label == 'Woman']]).reindex(DT_train.index)

# instantiate decision tree
myTree = tree.DecisionTreeClassifier(criterion = 'entropy', max_depth = 2)

# fit DT model
myTree.fit(DT_train, DT_train_label)

# define feature names
FeatureNames = DT_train.columns.values

# define class names
ClassNames = myTree.classes_

# visualize decision tree

# plot decision tree
plt.figure(figsize = (20, 10))
MyPlot = tree.plot_tree(myTree, feature_names = FeatureNames, class_names = ClassNames)
plt.show()

# create confusion matrix

# use decision tree to make predictions
DT_test_pred = myTree.predict(DT_test)

# build confusion matrix
conf_matrix = confusion_matrix(DT_test_label, DT_test_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = ClassNames)
disp.plot(cmap = 'Blues')
plt.show()

# calculate and print accuracy score

accuracy = accuracy_score(DT_test_label, DT_test_pred)
print(f"Accuracy: {accuracy:.2f}")