# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:39:47 2023

@author: jessi
"""

import geopandas as gpd
import pandas as pd

counties = gpd.read_file("cb_2022_us_county_20m.zip")

# filter to NYS
counties = counties.query("STATEFP=='36'")

# reproject NYS map image
counties = counties.to_crs(epsg=26918)

data=pd.read_pickle("youth_MHS.pkl")

#%%
merged = counties.merge(data,
                        left_on= "NAME",
                        right_on= "County",
                        how= "outer",
                        validate= "1:1",
                        indicator= True)
merged.drop(columns="_merge", inplace=True)

# Man not here 

merged.to_file("merged.gpkg",layer= "providers")

merged.plot("Psychologists", legend=True)
# wrap around matplotlib
# add label etc. 

