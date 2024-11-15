# -*- coding: utf-8 -*-
"""WIT_Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gR-DkFp8QhfxR3FnDVQuWBLmEuB8r7Gq
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

# drop specified columns
jobs_survey_Reg = jobs_survey.drop(columns = ['Unnamed: 0','HaveWorkedWith'])

# view dataframe
#jobs_survey_Reg.head()

# drop additional columns to perform analysis
jobs_survey_Reg = jobs_survey_Reg.drop(columns = ['EdLevel', 'MainBranch', 'Country'])
#jobs_survey_Reg.head()

# turning 'Accessibility' into Boolean
jobs_survey_Reg['Accessibility'] = jobs_survey_Reg['Accessibility'].replace({'No': 0})
jobs_survey_Reg['Accessibility'] = jobs_survey_Reg['Accessibility'].replace({'Yes': 1})

# turning 'MentalHealth' into Boolean
jobs_survey_Reg['MentalHealth'] = jobs_survey_Reg['MentalHealth'].replace({'No': 0})
jobs_survey_Reg['MentalHealth'] = jobs_survey_Reg['MentalHealth'].replace({'Yes': 1})

# view cleaned data
#jobs_survey_Reg.head()

# import libraries to create train/test sets
from sklearn.model_selection import train_test_split
from sklearn.utils import resample

# split data up into train and test sets
Reg_train, Reg_test = train_test_split(jobs_survey_Reg, test_size = .3, random_state = 1989)

# set label for train and test sets
Reg_train_label = Reg_train["Gender"]
Reg_test_label = Reg_test["Gender"]

# drop label
Reg_train = Reg_train.drop(["Gender"], axis=1)
Reg_test = Reg_test.drop(["Gender"], axis=1)

# execute oversample because women are underrepresented in dataset

# define majority and minority classes
majority_class = Reg_train[Reg_train_label == 'Man']
minority_class = Reg_train[Reg_train_label == 'Woman']

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace=True, n_samples=len(majority_class), random_state=1989)

# combine back to single train set
Reg_train = pd.concat([majority_class, minority_upsampled])
Reg_train_label = pd.concat([Reg_train_label[Reg_train_label == 'Man'], Reg_train_label[Reg_train_label == 'Woman']]).reindex(Reg_train.index)

# import libraries for logistic regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# instantiate logistic regression
my_log_reg = LogisticRegression()

# fit model
my_log_reg.fit(Reg_train, Reg_train_label)

# make predictions from fitted model
Reg_test_pred = my_log_reg.predict(Reg_test)

# calculate and print accuracy score (logreg)
accuracy = accuracy_score(Reg_test_label, Reg_test_pred)
print(f"Accuracy: {accuracy:.2f}")

# create confusion matrix for logreg

# import library
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# construct confusion matrix
conf_matrix = confusion_matrix(Reg_test_label, Reg_test_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=my_log_reg.classes_)
disp.plot(cmap='Blues')

# perform Multinomial Naive Bayes on same data

# import library
from sklearn.naive_bayes import MultinomialNB

# instantiate multinomial naive bayes
MyMN = MultinomialNB()

# fit model
MyMN_Model = MyMN.fit(Reg_train, Reg_train_label)

# make predictions from fitted model
MN_predict = MyMN_Model.predict(Reg_test)

# create confusion matrix for MN NB

# construct confusion matrix
conf_matrix = confusion_matrix(Reg_test_label, MN_predict)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=MyMN.classes_)
disp.plot(cmap='Blues')

# calculate and print accuracy score (MN NB)
accuracy = accuracy_score(Reg_test_label, MN_predict)
print(f"Accuracy: {accuracy:.2f}")