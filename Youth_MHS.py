# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:33:56 2023

@author: jessi
"""
# import necessary modules

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 300

#%% ACCESS CENSUS DATA

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

#%% CLEANING DATA & PREPARE DATA FOR A LEFT JOIN

# rename census columns to descriptive column headers
under_18_county = under_18_county.rename(columns={
    "B09001_001E": "POP", 
    "B01001_001E": "TOTAL_POP"})

# convert the POP column into integers
under_18_county["POP"]=under_18_county["POP"].astype(int)

# import CSV file for '2015 Behavioral Health Service Providers in NYS by County'
mental_health_2015 = pd.read_csv('Behavioral health service providers by county 2015.csv')

# replace county names to match CVS file- dropping the New York description
under_18_county['NAME'] = under_18_county['NAME'].str.replace(' County, New York', '')

# drop unnecesary columns
under_18_county= under_18_county.drop(columns= 'state')
under_18_county= under_18_county.drop(columns= 'county')

# rename columns with similar names in both datasets
under_18_county = under_18_county.rename(columns={"NAME": "County"})

# change CVS file name to match census data
mental_health_2015['County']= mental_health_2015['County'].replace('Saint Lawrence', 'St. Lawrence')

# merge data with a left hand join, merge onto county in this join
# created new dataframe with relevant information
youth_MHS = under_18_county.merge(mental_health_2015, left_on=["County"], right_on= ["County"], how= 'left')

#%% WORK WITH DATA

# can expand to look at ratios across different states
# create column with ration of population/ 10,000 kids
youth_MHS['POP_10K']= youth_MHS['POP']/10e3

# total youth oriented Psychiatrists
youth_MHS['TOTAL_PSY'] = youth_MHS['Psychiatrists'] * youth_MHS['POP']/10e3

# dropping Manhattan as an outlyer as this is not indicitive of the average data
# 
# drop unwanted row 
youth_MHS = youth_MHS.query("County != 'New York'")

#%%
# GRAPHING AND PLOTTING DATA
# various data visualization  methods can be seen below


#%% SCATTER PLOTS AND REGRESSIONS

# create scatter plot across Pediatricians & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Pediatricians', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.lmplot(x= 'Pediatricians', y='Psychiatrists', data=youth_MHS)

ax.set_title("Pediatricians and Psychiatrists")
ax.set_xlabel("Pediatricians")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Pediatricians and Psychiatrists.png")

#%%

# create scatter plot across Total Population & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Psychiatrists', ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
#sns.lmplot(x= 'TOTAL_POP', y='Psychiatrists', data=youth_MHS)

ax.set_title("Total Population of Psychiatrists NYS Counties")
ax.set_xlabel("Total Population")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Total Population of Psychiatrists NYS Counties")

#%% Psychologists

# create scatter plot across Total Population & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Psychologists', ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
#sns.lmplot(x= 'TOTAL_POP', y='Psychiatrists', data=youth_MHS)

ax.set_title("Total Population of Psychologists NYS Counties")
ax.set_xlabel("Total Population")
ax.set_ylabel("Psychologists")
fig.tight_layout()
fig.savefig("Total Population of Psychologists NYS Counties")

#%%

# create scatter plot across LSW & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Licensed Social Workers', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.lmplot(x= 'Licensed Social Workers', y='Psychiatrists', data=youth_MHS);


#%% HEX PLOT

# produces high-level graphics object that doesn't require the subplot function
# hex plot of LSW and Psychiatrists
jg = sns.jointplot( data=youth_MHS, x="Licensed Social Workers", y="Psychiatrists",
                   kind= "hex")

jg.set_axis_labels("Licensed Social Workers", "Psychiatrists")
jg.fig.suptitle("LSW & Psychiatrists")
jg.fig.tight_layout()
fig.savefig("LSW & Psychiatrists Hex.png")

#%% DENSITY PLOT

# stack data to create overlapping densities of different types of doctors availible
#
stacked = youth_MHS [['County', 'Pediatricians',
                      'Psychiatrists', 'Family Medicine Physicians',
                      'Licensed Social Workers','Psychologists']]

stacked = stacked.set_index("County")
stacked = stacked.stack().reset_index()
stacked = stacked.rename(columns= {"level_1": "Provider", 0:"Count"})

# create density plot of multiple providers
# plot reps the probability of finding a provdior that area, orange (Psychiatrists) 
# for example is a higher likelyhood, whereas pink (LSW) are spread all over the place

fig,ax = plt.subplots()
sns.kdeplot(data=stacked, x="Count", hue= "Provider", fill=True, ax=ax)
ax.set_title("Probability Density Multiple Providers")
fig.tight_layout()
fig.savefig("Probability Density Multiple Providers")





