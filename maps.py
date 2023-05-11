# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:39:47 2023

@author: jessi
"""

#%% IMPORT MODULES AS NECESSARY
import geopandas as gpd
import pandas as pd

#%% READ AND PROJECT DATA

# read in census shapefile containing all counties in the United States
counties = gpd.read_file("cb_2022_us_county_20m.zip")

# filter counties for only those in NYS
counties = counties.query("STATEFP=='36'")

# reproject NYS map image so we can create a heat map wihtin the counties
counties = counties.to_crs(epsg=26918)

data=pd.read_pickle("youth_MHS.pkl")

#%% CREATE MERGED DATAFRAME FOR MAPPING
# note we dropped Manhattan earlier as the outlyer, so we have
# no data for this county

# creating new dataframe, merge on the counties
merged = counties.merge(data,
                        left_on= "NAME",
                        right_on= "County",
                        how= "outer",
                        validate= "1:1",
                        indicator= True)

# drop the merged column
merged.drop(columns="_merge", inplace=True)

# create gpkg file to project into the county map
merged.to_file("merged.gpkg",layer= "providers")

#%% CREATE HEATMAP WITH DATAFRAME

# create providers map with informative legend
merged.plot("Psychologists", legend=True)

# create providers map with informative legend
merged.plot("Pediatricians", legend=True)

# create providers map with informative legend
merged.plot("Psychiatrists", legend=True)

# create providers map with informative legend
merged.plot("Licensed Social Workers", legend=True)

# wrap around matplotlib
# add label etc. 

