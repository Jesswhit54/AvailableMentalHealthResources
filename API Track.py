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

url = "https://api.census.gov/data/2021/acs/acs5"
params = {
    "get": "B09001_001E,NAME",
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
under_18_county = under_18_county.rename(columns={"B09001_001E": "POP"})

# convert POP column into integers
under_18_county["POP"]=under_18_county["POP"].astype(int)

# import CSV file for Behavioral health service providers by county in 2015
mental_health_2015 = pd.read_csv('Behavioral health service providers by county 2015.csv')

# merge data sets/ join data


