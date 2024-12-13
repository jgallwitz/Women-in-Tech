# -*- coding: utf-8 -*-
"""WIT_Ensemble.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CPzRsvb-ArhK8x12_A7h3b-ihqV2B0vk
"""

# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read in CSV file
SO_survey = pd.read_csv('/content/2019survey_results_public.csv')

# drop unnecessary columns
SO_survey = SO_survey.drop(columns = ['Respondent','OpenSourcer','FizzBuzz','ResumeUpdate','CurrencyDesc','CompFreq','WorkPlan','WorkRemote','WorkLoc',
                                      'CodeRevHrs','UnitTests','PurchaseHow','PurchaseWhat','LanguageDesireNextYear','DatabaseDesireNextYear',
                                      'PlatformWorkedWith','PlatformDesireNextYear','WebFrameWorkedWith','WebFrameDesireNextYear','MiscTechWorkedWith',
                                      'MiscTechDesireNextYear','DevEnviron','OpSys','Containers','BlockchainOrg','BlockchainIs','BetterLife','ITperson',
                                      'OffOn','SocialMedia','Extraversion','ScreenName','SOVisit1st','SOVisitFreq','SOVisitTo','SOFindAnswer','SOTimeSaved',
                                      'SOHowMuchTime','SOAccount','SOPartFreq','SOJobs','EntTeams','SOComm','SONewContent','Trans','Sexuality',
                                      'SurveyLength','SurveyEase', 'UndergradMajor','EduOther','OpenSourcer','Student','UndergradMajor','EduOther','OrgSize',
                                      'DevType', 'MgrIdiot', 'JobSeek', 'LastHireDate', 'LastInt', 'JobFactors', 'CurrencySymbol','CodeRev',
                                      'Ethnicity', 'MgrMoney', 'MgrWant','ConvertedComp', 'WorkWeekHrs', 'LanguageWorkedWith', 'DatabaseWorkedWith',
                                      'CompTotal','OpenSource', 'Dependents', 'EdLevel', 'JobSat','WelcomeChange'])

# dropping all rows that are outside of the US
SO_survey = SO_survey.drop(SO_survey[SO_survey['Country'] != 'United States'].index)

# dropping rows with no Gender response
SO_survey = SO_survey.dropna(subset=['Gender'])

# dropping rows that have a Gender response that's not 'Man' or 'Woman'
SO_survey = SO_survey.drop(SO_survey[~SO_survey['Gender'].isin(['Man', 'Woman'])].index)

# dropping rows where the respondent is not a developer by profession
SO_survey = SO_survey.drop(SO_survey[SO_survey['MainBranch'] != 'I am a developer by profession'].index)

# convert work challenges to boolean for whether they identified a toxic workplace
SO_survey['ToxicWorkEnv'] = SO_survey['WorkChallenge'].apply(lambda x: 1 if 'Toxic work environment' in str(x) else 0)

SO_survey.drop('WorkChallenge', axis=1, inplace=True)

# fille missing age values with average for those who have the same years of coding experience
SO_survey['Age'] = SO_survey.groupby('YearsCode')['Age'].transform(lambda x: x.fillna(x.mean()))

# drop NA values
SO_survey = SO_survey.dropna()

# reindex
SO_survey = SO_survey.reset_index(drop=True)

# view cleaned data
SO_survey.head()

# drop a few more columns to clean up
SO_survey = SO_survey.drop(columns = ['MainBranch','Country'])

# replace less than 1 year with 1
SO_survey['YearsCode'] = SO_survey['YearsCode'].replace('Less than 1 year', 1)
SO_survey['YearsCodePro'] = SO_survey['YearsCodePro'].replace('Less than 1 year', 1)

# ensure all values are integers
SO_survey['YearsCode'] = pd.to_numeric(SO_survey['YearsCode'], errors='coerce')
SO_survey['YearsCodePro'] = pd.to_numeric(SO_survey['YearsCodePro'], errors='coerce')

# same process for less than 5 years
SO_survey['Age1stCode'] = SO_survey['Age1stCode'].replace('Younger than 5 years', 5)
SO_survey['Age1stCode'] = pd.to_numeric(SO_survey['Age1stCode'], errors='coerce')

# encode categorical variables

SO_survey = pd.get_dummies(SO_survey, columns=['Hobbyist', 'Employment', 'CareerSat', 'ImpSyn'])

SO_survey.head()

# import libraries for RF
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

RF_train, RF_test = train_test_split(SO_survey, test_size = .3, random_state = 1989)

# set label for train and test sets
RF_train_label = RF_train["Gender"]
RF_test_label = RF_test["Gender"]

# drop label
RF_train = RF_train.drop(["Gender"], axis = 1)
RF_test = RF_test.drop(["Gender"], axis = 1)

# execute oversample because women are underrepresented in dataset

# import library to upsample
from sklearn.utils import resample

# define majority and minority classes
majority_class = RF_train[RF_train_label == 'Man']
minority_class = RF_train[RF_train_label == 'Woman']

# upsample with replacement
# balance classes
minority_upsampled = resample(minority_class, replace = True, n_samples = len(majority_class), random_state = 1989)

# combine back to single train set
RF_train = pd.concat([majority_class, minority_upsampled])
RF_train_label = pd.concat([RF_train_label[RF_train_label == 'Man'], RF_train_label[RF_train_label == 'Woman']]).reindex(RF_train.index)

# initialize RF
MyRF_model = RandomForestClassifier(n_estimators = 100, random_state = 2000)
MyRF_model.fit(RF_train, RF_train_label)

# make predictions with model
RF_pred = MyRF_model.predict(RF_test)

# create confusion matrix for RF

#import library
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# construct confusion matrix
conf_matrix = confusion_matrix(RF_test_label, RF_pred)

# display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = MyRF_model.classes_)
disp.plot(cmap = 'Blues')

#print accuracy score
print("Accuracy:", accuracy_score(RF_test_label, RF_pred))

# calculate and print classification report

from sklearn.metrics import classification_report

print(classification_report(RF_test_label, RF_pred))