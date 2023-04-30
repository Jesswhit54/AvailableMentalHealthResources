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

# replace 
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

# possibly good in theory but not Monday presentation?????????????????????????????????????
fig,ax = plt.subplots()
youth_MHS['Psychiatrists'].plot.barh(ax=ax)

#%% GRAPHING AND PLOTTING DATA

# create scatterplot 
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Pediatricians', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.lmplot(x= 'Pediatricians', y='Psychiatrists', data=youth_MHS)

#ax.set_title("Nameplate Capacity")
#ax1.set_xlabel("kW")
#ax1.set_ylabel("")
#fig.tight_layout()
#fig.savefig("res_kde.png")

fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Psychiatrists', ax=ax)


fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Licensed Social Workers', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.lmplot(x= 'Licensed Social Workers', y='Psychiatrists', data=youth_MHS);


# produces high-level graphics object that doesn't require the subplot function
jg = sns.jointplot( data=youth_MHS, x="Licensed Social Workers", y="Psychiatrists",
                   kind= "hex")
jg.set_axis_labels("Licensed Social Workers", "Psychiatrists")
# set overall title
jg.fig.suptitle("Test")
#jg.fig.tight_layout()
#fig.savefig("res_hexbin.png")

# distributions of social workers across counties 
# some counties have a large number 
fig,ax = plt.subplots()
sns.kdeplot(data=youth_MHS, x="Licensed Social Workers",   
            palette="Psychiatrists", fill=True, ax=ax)
ax.set_title("Test2")
ax.set_xlabel("1")
ax.set_ylabel("2")

#%%
# stack data to get overlapping densities of different drs availible in a density 

stacked = youth_MHS [['County', 'Pediatricians',
                      'Psychiatrists', 'Family Medicine Physicians',
                      'Licensed Social Workers','Psychologists']]
stacked = stacked.set_index("County")
stacked = stacked.stack().reset_index()
stacked = stacked.rename(columns= {"level_1": "Provider", 0:"Count"})

#%%
fig,ax = plt.subplots()
sns.kdeplot(data=stacked, x="Count", hue= "Provider", fill=True, ax=ax)

# probability density- higher probablity of grabbign number in orange
# and get a provider but social workers could be all over the place






