# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:33:56 2023

@author: jessi
"""

#%% IMPORT NECESSARY MODULES
# import modules to read and clean data

import requests
import pandas as pd

#%% ACCESS AND READ CENSUS DATA

# create API to access census data (you will need to request a census key)
url = "https://api.census.gov/data/2015/acs/acs5"
params = {
    "get": "B09001_001E,NAME,B01001_001E,B19113_001E",
    "for": "county:*",
    "in": "state:36", # change state you are requesting information for here
    "key": '37233c863bd5ebadbea1db94fdea521aa5ad4ddd'
    }

#Send GET request to API and retrieve JSON response
response = requests.get(url, params=params)
json_data = response.json()

#Parse JSON response and extract relevant data
headers = json_data[0]
data = json_data[1:]
census_2015 = pd.DataFrame(columns=headers, data=data)

#%% CLEANING DATA TO PREPARE FOR MERGE

# rename the census columns to descriptive column headers
census_2015 = census_2015.rename(columns={
    "B09001_001E": "POP", 
    "B01001_001E": "TOTAL_POP",
    "B19113_001E": "FAM_INCOME"})

# convert any columns containing numbers from strings into integers via a loop
# you cannot run regressions on string variables
for column in ["POP", "TOTAL_POP", "FAM_INCOME"]:
    census_2015[column]=census_2015[column].astype(int)


# import CSV file for '2015 Behavioral Health Service Providers in NYS by County'
mental_health_2015 = pd.read_csv('Behavioral health service providers by county 2015.csv')


# replace county names to match CVS file- dropping the New York description
census_2015['NAME'] = census_2015['NAME'].str.replace(' County, New York', '')


# drop unnecesary columns
census_2015 = census_2015.drop(columns= 'state')
census_2015= census_2015.drop(columns= 'county')


# rename columns with similar names in both datasets
census_2015 = census_2015.rename(columns={"NAME": "County"})


# change CVS file name to match census data
mental_health_2015['County']= mental_health_2015['County'].replace('Saint Lawrence', 'St. Lawrence')
#%% MERGE DATA- LEFT JOIN DATA

# merge data with a left hand join, merge onto county in this join
# created new dataframe with relevant information
youth_MHS = census_2015.merge(mental_health_2015, left_on=["County"], right_on= ["County"], how= 'left')

#%% CALCULATING RATIOS WITHIN DATA

# can expand to look at ratios across different states
# create column with ration of population/ 10,000 kids
youth_MHS['POP_10K']= youth_MHS['POP']/10e3

# total youth oriented Psychiatrists
youth_MHS['TOTAL_PSY'] = youth_MHS['Psychiatrists'] * youth_MHS['POP']/10e3

# I amdropping Manhattan as an outlyer as this is not indicitive of the average data
# remove this line if not you'd like to view all variables

# drop unwanted row 
youth_MHS = youth_MHS.query("County != 'New York'")

#%% SAVING DATA FILE

youth_MHS.to_pickle("youth_MHS.pkl")







