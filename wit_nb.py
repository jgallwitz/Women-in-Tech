# -*- coding: utf-8 -*-
"""WIT_NB.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aVreT_KKP5I7PcCUV6ZCpVIlin2ew6pk
"""

# import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read in CSV file and view dataset
jobs_survey = pd.read_csv('/content/job_survey.csv')
#jobs_survey.head()

# dropping all rows that are outside of the US
jobs_survey = jobs_survey.drop(jobs_survey[jobs_survey['Country'] != 'United States of America'].index)

# dropping all NonDev employees
jobs_survey = jobs_survey.drop(jobs_survey[jobs_survey['MainBranch'] != 'Dev'].index)

# drop all nonbinary respondents since I want to compare men and women
jobs_survey = jobs_survey.drop(jobs_survey[jobs_survey['Gender'] == 'NonBinary'].index)

# reindexing
jobs_survey = jobs_survey.reset_index(drop=True)

# drop specified columns
jobs_survey = jobs_survey.drop(columns = ['Unnamed: 0'])

# drop qualitative columns as they are not conducive to performing Multinomial Naive Bayes
jobs_survey_MN_NB = jobs_survey.drop(columns = ['Age', 'EdLevel','Employment','Employed','MentalHealth','MainBranch','Country', 'Accessibility', 'HaveWorkedWith'])
#jobs_survey_MN_NB.head()

# import libraries for Multinomial NB
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.preprocessing import OrdinalEncoder

# Multinomial NB
# split data up into train and test sets
MN_train, MN_test = train_test_split(jobs_survey_MN_NB, test_size = .3, random_state = 2024)

# set label for train and test sets
MN_train_label = MN_train["Gender"]
MN_test_label = MN_test["Gender"]

# drop label
MN_train = MN_train.drop(["Gender"], axis = 1)
MN_test = MN_test.drop(["Gender"], axis = 1)

# execute oversample because women are underrepresented in dataset

# import library to upsample
from sklearn.utils import resample

# define majority and minority classes
majority_class = MN_train[MN_train_label == 'Man']
minority_class = MN_train[MN_train_label == 'Woman']

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace = True, n_samples = len(majority_class), random_state = 1989)

# combine back to single train set
MN_train = pd.concat([majority_class, minority_upsampled])
MN_train_label = pd.concat([MN_train_label[MN_train_label == 'Man'], MN_train_label[MN_train_label == 'Woman']]).reindex(MN_train.index)

# instantiate MN NB
MyMN = MultinomialNB()

# fit MN NB model
MyMN_Model = MyMN.fit(MN_train, MN_train_label)

MN_predict = MyMN_Model.predict(MN_test)

# create confusion matrix for MN NB

# import library for confusion matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# construct confusion matrix
conf_matrix = confusion_matrix(MN_test_label, MN_predict)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = MyMN.classes_)
disp.plot(cmap = 'Blues')

# calculate accuracy score
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(MN_test_label, MN_predict)
(f"Accuracy: {accuracy:.2f}")

#jobs_survey.head()

jobs_survey_BNB = jobs_survey.drop(columns = ['MainBranch','Country', 'YearsCode','HaveWorkedWith'])

#jobs_survey_BNB.head()

# turning 'Gender' into Boolean
jobs_survey_BNB['Gender'] = jobs_survey_BNB['Gender'].replace({'Man': 0})
jobs_survey_BNB['Gender'] = jobs_survey_BNB['Gender'].replace({'Woman': 1})


# turning 'Accessibility' into Boolean
jobs_survey_BNB['Accessibility'] = jobs_survey_BNB['Accessibility'].replace({'No': 0})
jobs_survey_BNB['Accessibility'] = jobs_survey_BNB['Accessibility'].replace({'Yes': 1})


# turning 'MentalHealth' into Boolean
jobs_survey_BNB['MentalHealth'] = jobs_survey_BNB['MentalHealth'].replace({'No': 0})
jobs_survey_BNB['MentalHealth'] = jobs_survey_BNB['MentalHealth'].replace({'Yes': 1})


# turning 'Age' into Boolean
jobs_survey_BNB['Age'] = jobs_survey_BNB['Age'].replace({'<35': 0})
jobs_survey_BNB['Age'] = jobs_survey_BNB['Age'].replace({'>35': 1})

# turning 'Accessibility' into Boolean
jobs_survey_BNB['Accessibility'] = jobs_survey_BNB['Accessibility'].replace({'No': 0})
jobs_survey_BNB['Accessibility'] = jobs_survey_BNB['Accessibility'].replace({'Yes': 1})


# turning 'MentalHealth' into Boolean
jobs_survey_BNB['MentalHealth'] = jobs_survey_BNB['MentalHealth'].replace({'No': 0})
jobs_survey_BNB['MentalHealth'] = jobs_survey_BNB['MentalHealth'].replace({'Yes': 1})


# turning 'Age' into Boolean
jobs_survey_BNB['Age'] = jobs_survey_BNB['Age'].replace({'<35': 0})
jobs_survey_BNB['Age'] = jobs_survey_BNB['Age'].replace({'>35': 1})


# turning 'Edlevel' into Boolean
jobs_survey_BNB['EdLevel'] = jobs_survey_BNB['EdLevel'].replace({'Undergraduate': 0})
jobs_survey_BNB['EdLevel'] = jobs_survey_BNB['EdLevel'].replace({'Other': 0})
jobs_survey_BNB['EdLevel'] = jobs_survey_BNB['EdLevel'].replace({'NoHigherEd': 0})
jobs_survey_BNB['EdLevel'] = jobs_survey_BNB['EdLevel'].replace({'PhD': 1})
jobs_survey_BNB['EdLevel'] = jobs_survey_BNB['EdLevel'].replace({'Master': 1})


# turning 'YearsCodePro' into a Boolean where 0 is less than 10 years of experience
jobs_survey_BNB['YearsCodePro'] = np.where(jobs_survey_BNB['YearsCodePro'] > 10, 1, 0)


# turning 'ComputerSkills' into a Boolean where 0 is less than 10 computer skills
jobs_survey_BNB['ComputerSkills'] = np.where(jobs_survey_BNB['ComputerSkills'] > 10, 1, 0)


# turning 'PreviousSalary' into a Boolean where 0 is a previous salary of less than $100,000
jobs_survey_BNB['PreviousSalary'] = np.where(jobs_survey_BNB['PreviousSalary'] > 100000, 1, 0)

BNB_train, BNB_test = train_test_split(jobs_survey_BNB, test_size = .3, random_state = 1996)

# set label for train and test sets
BNB_train_label = BNB_train["Gender"]
BNB_test_label = BNB_test["Gender"]

# drop label
BNB_train = BNB_train.drop(["Gender"], axis = 1)
BNB_test = BNB_test.drop(["Gender"], axis = 1)

# execute oversample because women are underrepresented in dataset

# define majority and minority classes
majority_class = BNB_train[BNB_train_label == 0]
minority_class = BNB_train[BNB_train_label == 1]

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace=True, n_samples = len(majority_class), random_state = 1996)

# combine back to single train set
BNB_train = pd.concat([majority_class, minority_upsampled])
BNB_train_label = pd.concat([BNB_train_label[BNB_train_label == 0], BNB_train_label[BNB_train_label == 1]]).reindex(BNB_train.index)

# Bernoulli Naive Bayes

# import BNB library
from sklearn.naive_bayes import BernoulliNB

# instantiate Bernoulli Naive Bayes
MyBNB = BernoulliNB()

# fit MN NB model
MyBNB_Model = MyBNB.fit(BNB_train, BNB_train_label)

BNB_predict = MyBNB_Model.predict(BNB_test)

# create confusion matrix for Bernoulli NB

# construct confusion matrix
conf_matrix = confusion_matrix(BNB_test_label, BNB_predict)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = MyBNB.classes_)
disp.plot(cmap = 'Blues')

# calculate and print accuracy score

accuracy = accuracy_score(BNB_test_label, BNB_predict)
(f"Accuracy: {accuracy:.2f}")

#jobs_survey.head()

jobs_survey_CNB = jobs_survey.drop(columns = ['YearsCode', 'Country', 'MainBranch'])

# turning 'Gender' into Boolean
jobs_survey_CNB['Gender'] = jobs_survey_CNB['Gender'].replace({'Man': 0})
jobs_survey_CNB['Gender'] = jobs_survey_CNB['Gender'].replace({'Woman': 1})


# turning 'Accessibility' into Boolean
jobs_survey_CNB['Accessibility'] = jobs_survey_CNB['Accessibility'].replace({'No': 0})
jobs_survey_CNB['Accessibility'] = jobs_survey_CNB['Accessibility'].replace({'Yes': 1})


# turning 'MentalHealth' into Boolean
jobs_survey_CNB['MentalHealth'] = jobs_survey_CNB['MentalHealth'].replace({'No': 0})
jobs_survey_CNB['MentalHealth'] = jobs_survey_CNB['MentalHealth'].replace({'Yes': 1})


# turning 'Age' into Boolean
jobs_survey_CNB['Age'] = jobs_survey_CNB['Age'].replace({'<35': 0})
jobs_survey_CNB['Age'] = jobs_survey_CNB['Age'].replace({'>35': 1})

# turning 'Accessibility' into Boolean
jobs_survey_CNB['Accessibility'] = jobs_survey_CNB['Accessibility'].replace({'No': 0})
jobs_survey_CNB['Accessibility'] = jobs_survey_CNB['Accessibility'].replace({'Yes': 1})


# turning 'MentalHealth' into Boolean
jobs_survey_CNB['MentalHealth'] = jobs_survey_CNB['MentalHealth'].replace({'No': 0})
jobs_survey_CNB['MentalHealth'] = jobs_survey_CNB['MentalHealth'].replace({'Yes': 1})


# turning 'Age' into Boolean
jobs_survey_CNB['Age'] = jobs_survey_CNB['Age'].replace({'<35': 0})
jobs_survey_CNB['Age'] = jobs_survey_CNB['Age'].replace({'>35': 1})


# turning 'Edlevel' into Boolean
jobs_survey_CNB['EdLevel'] = jobs_survey_CNB['EdLevel'].replace({'Undergraduate': 0})
jobs_survey_CNB['EdLevel'] = jobs_survey_CNB['EdLevel'].replace({'Other': 0})
jobs_survey_CNB['EdLevel'] = jobs_survey_CNB['EdLevel'].replace({'NoHigherEd': 0})
jobs_survey_CNB['EdLevel'] = jobs_survey_CNB['EdLevel'].replace({'PhD': 1})
jobs_survey_CNB['EdLevel'] = jobs_survey_CNB['EdLevel'].replace({'Master': 1})


# turning 'YearsCodePro' into a Boolean where 0 is less than 10 years of experience
jobs_survey_CNB['YearsCodePro'] = np.where(jobs_survey_CNB['YearsCodePro'] > 10, 1, 0)


# turning 'ComputerSkills' into a Boolean where 0 is less than 10 computer skills
jobs_survey_CNB['ComputerSkills'] = np.where(jobs_survey_CNB['ComputerSkills'] > 10, 1, 0)


# turning 'PreviousSalary' into a Boolean where 0 is a previous salary of less than $100,000
jobs_survey_CNB['PreviousSalary'] = np.where(jobs_survey_CNB['PreviousSalary'] > 100000, 1, 0)

#jobs_survey_CNB.head()

# binarize haveworkedwith column

# import multilabelbinarizer library
from sklearn.preprocessing import MultiLabelBinarizer

# convert column to string
jobs_survey_CNB['HaveWorkedWith'] = jobs_survey_CNB['HaveWorkedWith'].fillna('').astype(str)

# split the values in the column by ";"
jobs_survey_CNB['HaveWorkedWith'] = jobs_survey_CNB['HaveWorkedWith'].apply(lambda x: x.split(';'))

#initialize mlb
mlb = MultiLabelBinarizer()

# apply transformation
jobs_survey_CNB_transformed = pd.DataFrame(mlb.fit_transform(jobs_survey_CNB['HaveWorkedWith']), columns = mlb.classes_, index = jobs_survey_CNB.index)

# combine with full dataframe
jobs_survey_CNB = pd.concat([jobs_survey_CNB.drop('HaveWorkedWith', axis=1), jobs_survey_CNB_transformed], axis = 1)

CNB_train, CNB_test = train_test_split(jobs_survey_CNB, test_size = .3, random_state = 2001)

# set label for train and test sets
CNB_train_label = CNB_train["Gender"]
CNB_test_label = CNB_test["Gender"]

# drop label
CNB_train = CNB_train.drop(["Gender"], axis=1)
CNB_test = CNB_test.drop(["Gender"], axis=1)

# execute oversample because women are underrepresented in dataset

# define majority and minority classes
majority_class = CNB_train[CNB_train_label == 0]
minority_class = CNB_train[CNB_train_label == 1]

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace = True, n_samples = len(majority_class), random_state = 2001)

# combine back to single train set
CNB_train = pd.concat([majority_class, minority_upsampled])
CNB_train_label = pd.concat([CNB_train_label[CNB_train_label == 0], CNB_train_label[CNB_train_label == 1]]).reindex(CNB_train.index)

# Categorical Naive Bayes

# import library
from sklearn.naive_bayes import CategoricalNB

# instantiate categorical naive bayes
MyCNB = CategoricalNB()

# fit CNB model
MyCNB_Model = MyCNB.fit(CNB_train, CNB_train_label)

CNB_predict = MyCNB_Model.predict(CNB_test)

# create confusion matrix for Categorical NB

# construct confusion matrix
conf_matrix = confusion_matrix(CNB_test_label, CNB_predict)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = MyCNB.classes_)
disp.plot(cmap = 'Blues')

# calculate and print accuracy score

accuracy = accuracy_score(CNB_test_label, CNB_predict)
(f"Accuracy: {accuracy:.2f}")