# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:33:56 2023

@author: jessi
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 300

# create API to access census data (you will need to request a census key)
url = "https://api.census.gov/data/2015/acs/acs5"
params = {
    "get": "B09001_001E,NAME,B01001_001E",
    "for": "county:*",
    "in": "state:36",
    "key": '37233c863bd5ebadbea1db94fdea521aa5ad4ddd'
    }

#Send GET request to API and retrieve JSON response
response = requests.get(url, params=params)
json_data = response.json()

#Parse JSON response and extract relevant data
headers = json_data[0]
data = json_data[1:]

under_18_county = pd.DataFrame(columns=headers, data=data)

# rename census column into POP= population
under_18_county = under_18_county.rename(columns={
    "B09001_001E": "POP", 
    "B01001_001E": "TOTAL_POP"})

# convert POP column into integers
under_18_county["POP"]=under_18_county["POP"].astype(int)

# import CSV file for Behavioral health service providers by county in 2015
mental_health_2015 = pd.read_csv('Behavioral health service providers by county 2015.csv')


under_18_county['NAME'] = under_18_county['NAME'].str.replace(' County, New York', '')

# drop unnecesary column
under_18_county= under_18_county.drop(columns= 'state')
under_18_county= under_18_county.drop(columns= 'county')

# rename column
under_18_county = under_18_county.rename(columns={"NAME": "County"})

# change CVS file name
mental_health_2015['County']= mental_health_2015['County'].replace('Saint Lawrence', 'St. Lawrence')

# merge data sets/ join data
youth_MHS = under_18_county.merge(mental_health_2015, left_on=["County"], right_on= ["County"], how= 'left')

# column with POP/ 10 K to compare numbers of providors and number of 10K kids
# look at ratios of these things across diff states

youth_MHS['POP_10K']= youth_MHS['POP']/10e3

# total psy kid oriented drs
youth_MHS['TOTAL_PSY'] = youth_MHS['Psychiatrists'] * youth_MHS['POP']/10e3
#%%
fig,ax = plt.subplots()
youth_MHS['Psychiatrists'].plot.barh(ax=ax)

fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Pediatricians', y='Psychiatrists',ax=ax)

# run regression, and access other variables that could affect these outcomes, 
# could get another variable such as per capita income. 

# look upseaborn lmplot and reg plot to appox regression. 

# sns.lmplot(data=None, x=None, y=None, hue=None, col=None, row=None, 
#               palette=None, col_wrap=None, height=5, aspect=1, markers='o', 
 #              sharex=None, sharey=None, hue_order=None, col_order=None, 
  #             row_order=None, legend=True, legend_out=None, x_estimator=None,
   #            x_bins=None, x_ci='ci', scatter=True, fit_reg=True, 
    #           ci=95, n_boot=1000, units=None, seed=None, order=1, 
     #          logistic=False, lowess=False, robust=False, logx=False, 
      #         x_partial=None, y_partial=None, truncate=True, x_jitter=None,
       #        y_jitter=None, scatter_kws=None, line_kws=None, facet_kws=None)

sns.regplot(data=youth_MHS)














