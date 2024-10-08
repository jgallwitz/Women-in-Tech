# -*- coding: utf-8 -*-
"""SOSurvey_Prep/EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14qQ9eAH_pRXiQD4HgFUDY-8jbW3cQNP6

Stack Overflow Data
"""

# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# read in CSV file
SO_survey = pd.read_csv('/content/2019survey_results_public.csv')

# view dataset
SO_survey.head()

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

# view value counts for gender
SO_survey['Gender'].value_counts()

# view value counts for country
SO_survey['Country'].value_counts()

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

# view value counts for toxic work env.
SO_survey['ToxicWorkEnv'].value_counts()

# fille missing age values with average for those who have the same years of coding experience
SO_survey['Age'] = SO_survey.groupby('YearsCode')['Age'].transform(lambda x: x.fillna(x.mean()))

# check for NA values
SO_survey.isna().sum()

# sum NA values
SO_survey.isna().any(axis=1).sum()

# drop NA values
SO_survey = SO_survey.dropna()

# check to ensure NA values were dropped
SO_survey.isna().sum()

# reindex
SO_survey = SO_survey.reset_index(drop=True)

# view cleaned data
SO_survey.head()

# create pie charts for percentage of men and women who identified a toxic work environment

SO_survey_men = SO_survey[SO_survey['Gender'] == 'Man']
SO_survey_women = SO_survey[SO_survey['Gender'] == 'Woman']

men_toxic_counts = SO_survey_men['ToxicWorkEnv'].value_counts()
women_toxic_counts = SO_survey_women['ToxicWorkEnv'].value_counts()

labels = ['No', 'Yes']

fig, ax = plt.subplots(1, 2, figsize=(8, 6))

ax[0].pie(men_toxic_counts, labels=labels, autopct='%1.1f%%', startangle=90)
ax[0].set_title('Men - Toxic Work Environment')

ax[1].pie(women_toxic_counts, labels=labels, autopct='%1.1f%%', startangle=90)
ax[1].set_title('Women - Toxic Work Environment')

# create box plots to show distribution of age when first coded, grouped by gender

SO_survey['Age1stCode'] = pd.to_numeric(SO_survey['Age1stCode'], errors='coerce')

plt.figure(figsize=(8, 6))
sns.boxplot(y='Gender', x='Age1stCode', data=SO_survey)

plt.title('Distribution of Age First Coded by Gender')
plt.xlabel('Age First Coded')
plt.ylabel('Gender')

# create bar plots to show career satisfaction by gender

plt.figure(figsize=(8, 6))

sns.countplot(y='CareerSat', hue='Gender', data=SO_survey)

plt.title('Career Satisfaction by Gender')
plt.xlabel('Count')
plt.ylabel('Career Satisfaction')

# create bar plots to show career confidence by gender

plt.figure(figsize=(8, 6))

sns.countplot(y='ImpSyn', hue='Gender', data=SO_survey)

plt.title('Rated Level of Confidence by Gender')
plt.xlabel('Count')
plt.ylabel('Rated Level of Confidence')