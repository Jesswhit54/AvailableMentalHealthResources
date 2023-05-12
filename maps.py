# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:39:47 2023

@author: jessi
"""

#%% IMPORT MODULES AS NECESSARY
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300

#%% READ AND PROJECT DATA

# read in census shapefile containing all counties in the United States
counties = gpd.read_file("cb_2022_us_county_20m.zip")

# filter counties for only those in NYS
counties = counties.query("STATEFP=='36'")

# reproject NYS map image so we can create a heat map wihtin the counties
counties = counties.to_crs(epsg=26918)

#%% READ IN DATAFRAME
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

#%% CREATE HEATMAP COMPARISON WITH DATAFRAME

# set variable for merged data
state= merged.dissolve()

# set figure up for comparison plots
fig,((axul,axur),(axll,axlr))= plt.subplots(2,2)

# create providers map with informative legend
# set the color of the map with the cmap= command
# set the title of the map
# set outline boarder for New york with color, line width and which quandrent the image is assigned
# repeat steps for each map

merged.plot("Pediatricians",cmap="Purples", legend=True, ax=axul)
axul.axis("off")
axul.set_title("Pediatricians")
state.boundary.plot(color="grey",lw=0.25, ax=axul)

merged.plot("Psychologists",cmap="Blues", legend=True, ax=axur)
axur.axis("off")
axur.set_title("Psychologists")
state.boundary.plot(color="grey",lw=0.25, ax=axur)


merged.plot("Psychiatrists", cmap="Greens", legend=True, ax=axll)
axll.axis("off")
axll.set_title("Psychiatrists")
state.boundary.plot(color="grey",lw=0.25, ax=axll)

merged.plot("Licensed Social Workers",cmap="Oranges", legend=True, ax=axlr)
axlr.axis("off")
axlr.set_title("Licensed Social Workers")
state.boundary.plot(color="grey",lw=0.25, ax=axlr)

# set tight figure to make image easier to read
# save figure
fig.tight_layout()
fig.savefig("Images/ComparativeHeatMaps.png")



