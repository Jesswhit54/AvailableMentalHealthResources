# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:21:00 2023

@author: jessi
"""

#%% IMPORT NECESSARY MODULES
# import previous modules and data vizualization modules

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 300

#%% READING THE DATA

# Read your data file 
youth_MHS = pd.read_pickle("youth_MHS.pkl")

#%% GRAPHING AND PLOTTING DATA

# various data visualization  methods can be seen below

#%% PROVIDER CORRELATIONS
# we will look at various corrilations between the five providers

#%% SCATTER PLOTS AND REGRESSIONS

# Pediatricians & Psychiatrists
# 
# create a scatterplot across Pediatricians & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Pediatricians', y='Psychiatrists',ax=ax)




# CLEAN THIS
# run a regression on the scatterplot with a 95% confidence interval
sns.regplot(x='Pediatricians', y='Psychiatrists', data=youth_MHS, ax=ax)

# Is there a way to save image with regression???????????????????

ax.set_title( "Pediatricians & Psychiatrists")
ax.set_xlabel("Pediatricians")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Images/PediatriciansandPsychiatrists.png")
#%%
# Licensed Social Workers & Psychiatrists
# 
# create a scatterplot across LSW & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Licensed Social Workers', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.regplot(x= 'Licensed Social Workers', y='Psychiatrists', data=youth_MHS, ax=ax);

ax.set_title( "Licensed Social Workers & Psychiatrists")
ax.set_xlabel("Licensed Social Workers")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Images/Licensed SocialWorkersandPsychiatrists.png")

#%% CREATE 2 PANEL GRAPH FOR COMPARISON

fig1, (ax1,ax2) = plt.subplots(1,2, sharey=True)
fig1.suptitle("Psychiatrists Correlation")

#ax1.plot("Pediatricians", "Psychiatrists")
#ax2.plot("Licensed Social Workers", "Psychiatrists")

# create variable for x and y bar

youth_MHS.plot.scatter(ax=ax1, x="Pediatricians", y="Psychiatrists")
ax1.set_xlabel("Pediatricians")
ax1.set_ylabel("Psychiatrists")


youth_MHS.plot.scatter(ax=ax2, x="Licensed Social Workers", y="Psychiatrists")
ax2.set_xlabel("Licensed Social Workers")
ax2.set_ylabel("Psychiatrists")
fig1.tight_layout()

# add regressiion?????????????


#%% TOTAL POPULATION COMPARISONS

# create scatter plot across Total Population & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Psychiatrists', ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.lmplot(x= 'TOTAL_POP', y='Psychiatrists', data=youth_MHS)
sns.lmplot(x= 'FAM_INCOME', y='Psychiatrists', data=youth_MHS)


ax.set_title("Total Population of NYS Counties")
ax.set_xlabel("Total Population")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Images/TotalPopulationofNYSCounties.png")

#%% SEABORN RELPLOT

# The sizes argument sets the minimum and maximum sizes that will be used
# for points (which are scaled by the population of each ring). 
# The facet_kws argument is a dictionary of tweaks allowed by Seaborn's 
# FacetGrid objects: the 'despine' argument says not to remove the top 
# and right borders of the graph, and the subplot_kws is a dictionary of 
# tweaks that are passed on to the underlying matplotlib routines (here 
# it just adds a title). 


fg = sns.relplot(data= youth_MHS, x='FAM_INCOME', y= 'Psychiatrists',
                 size='POP', sizes=(10,200),
                 facet_kws={'despine': False, 
                            'subplot_kws': {'title': 'Family Income by Psychiatrists'}})
fig.savefig("Images/FamilyIncomebyPsychiatrists.png")


#%% SEABORN RELPLOT

fg = sns.relplot(data= youth_MHS, x='FAM_INCOME', y= 'Licensed Social Workers',
                 size='POP', sizes=(10,200),
                 facet_kws={'despine': False, 
                            'subplot_kws': {'title': 'Family Income by LSW'}})


#%% HEX PLOT

# produces high-level graphics object that doesn't require the subplot function
# hex plot of LSW and Psychiatrists
jg = sns.jointplot( data=youth_MHS, x="Licensed Social Workers", y="Psychiatrists",
                   kind= "hex")
jg.set_axis_labels("Licensed Social Workers", "Psychiatrists")
jg.fig.suptitle("LSW & Psychiatrists")
jg.fig.tight_layout()
jg.savefig("Images/LSWandPsychiatristsHex.png")

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
ax.set_title("Probability Desnity Multiple Providers")
fig.tight_layout()
fig.savefig("Images/ProbabilityDensityMultipleProviders.png")


#%% HEATMAP
# load in shape file- counties
# merge on to county whatever you want to use as color variable
# join onto county name
# geodataframe.plot("column name you want to use for coloring")
# 
# download shape file from census for cartigraphic boundreis for 
# county filter for FIPS code 36
# can tell ppl how to get original data 

# load whole thing and filter to State 36

#%%
# Look at quick reference 
# plt.subplots(1,2)

# seaborn can draw 4 plots in one thing later
# do ordinary plots one by one--- then do fancy later

# question, input data, how to run your scripts and the take away for readers-> heres the conclusion of who runs the risk of lacking 
# read me can contain all that or not. 
# read me file- beginning shoul tell the person who stumbles on your repositroty what they are lookign at 

