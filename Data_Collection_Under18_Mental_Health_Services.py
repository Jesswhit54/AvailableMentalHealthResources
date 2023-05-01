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


#%% SAVING THE FILE

youth_MHS.to_pickle("youth_MHS.pkl")







