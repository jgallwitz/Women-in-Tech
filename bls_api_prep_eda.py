# -*- coding: utf-8 -*-
"""BLS_API_Prep/EDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OHxiAIlOYjQ7x0SULrYFYD9-IXpW59m0
"""

import requests
import json
import pandas as pd

# my unique API key for BLS
api_key = "YOUR API KEY HERE"

# series IDs, unique IDs specific to the BLS API that allow me to pull certain data
series_ids = {
    # median weekly earnings, computer and mathematical jobs, men
    "men": "LEU0254530800",
    # median weekly earnings, computer and mathematical jobs, women
    "women": "LEU0254530900"
}

# define year ranges as BLS API only allows 40 data points per request
year_ranges = [
    (2000, 2019),
    (2020, 2023)
]

# build function to gather data from the BLS API
def fetch_bls_data(start_year, end_year):
  # define headers for request
  headers = {'Content-type': 'application/json'}
  # build request structure
  data = json.dumps({
      "seriesid": list(series_ids.values()),
      "startyear": str(start_year),
      "endyear": str(end_year),
      "registrationkey": api_key
      })
  # send request to BLS API
  response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
  # return response in JSON format
  return json.loads(response.text)

# create empty list to store data
combined_data = []

# loop through specified years and gather data
for start_year, end_year in year_ranges:
  # calls function to gather data from BLS API
  json_data = fetch_bls_data(start_year, end_year)
  # check if the response results are valid
  if json_data and 'Results' in json_data and 'series' in json_data['Results']:
    # loops through each series
    for series in json_data['Results']['series']:
      # determine gender based on series ID
      gender = "men" if series['seriesID'] == series_ids['men'] else "women"
      # iterate over data in the series
      for item in series.get('data', []):
        # include data for A01 period (entire year)
        if item['period'] == 'A01':
          # append data to list
          combined_data.append({
              'Year': item['year'],
              'Gender': gender,
              'Value': item['value']
              })

# sort data by year, then gender
combined_data.sort(key=lambda x: (x['Year'], x['Gender']))

# convert data to CSV
median_tech_earnings = pd.DataFrame(combined_data)

# export CSV
median_tech_earnings.to_csv('median_tech_earnings.csv', index=False)

# read CSV and view as a table
median_tech_earnings = pd.read_csv('/content/median_tech_earnings.csv')
#median_tech_earnings.head()

# confirm no missing values
median_tech_earnings.isnull().sum()

# explore dataset
median_tech_earnings.info()

# create column for yearly earnings by multiplying weekly earnings * 52

median_tech_earnings['Median Yearly Earnings'] = median_tech_earnings['Value'] * 52
median_tech_earnings.head()

# create column for salary differential by subtracting female median salary from male median salary for each year
differential_df = median_tech_earnings.pivot(index='Year', columns='Gender', values='Median Yearly Earnings')

differential_df['Differential'] = differential_df['men'] - differential_df['women']

# merge to master dataset
median_tech_earnings = median_tech_earnings.merge(differential_df[['Differential']], on='Year')

import seaborn as sns
import matplotlib.pyplot as plt

# create lineplot for median yearly earnings by gender

sns.set(style="ticks")

plt.figure(figsize=(8, 6))
sns.lineplot(data=median_tech_earnings, x='Year', y='Median Yearly Earnings', hue='Gender')

plt.title('Median Yearly Earnings for Men and Women in the Tech Sector')
plt.xlabel('Year')
plt.ylabel('Median Yearly Earnings ($)')

# create barplot for earnings differential

colors = ['orange' if val > 0 else 'blue' for val in differential_df['Differential']]

plt.figure(figsize=(10, 6))
sns.barplot(x=differential_df.index, y=differential_df['Differential'], palette = colors)

plt.title('Median Yearly Salary Differential Between Men and Women')
plt.xlabel('Year')
plt.ylabel('Salary Differential (Men - Women)($)')

plt.xticks(rotation=45)

plt.show()
