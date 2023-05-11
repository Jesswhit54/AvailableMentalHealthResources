# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:21:00 2023

@author: jessi
"""
# GRAPHING AND PLOTTING DATA
# various data visualization  methods can be seen below

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

#%% PROVIDER CORRELATIONS: SCATTERPLOT and REGRESSIONS
# we will look at various corrilations between the five providers

#%% Pediatricians & Psychiatrists

# create a scatterplot across Pediatricians & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Pediatricians', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval to display on graph
sns.regplot(x='Pediatricians', y='Psychiatrists', data=youth_MHS, ax=ax)

# saving the image with the regression model
ax.set_title( "Pediatricians & Psychiatrists")
ax.set_xlabel("Pediatricians")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Images/PediatriciansandPsychiatrists.png")

#%% Licensed Social Workers & Psychiatrists
 
# create a scatterplot across LSW & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Licensed Social Workers', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval to display on graph
sns.regplot(x= 'Licensed Social Workers', y='Psychiatrists', data=youth_MHS, ax=ax);

# saving the image with the regression model
ax.set_title( "Licensed Social Workers & Psychiatrists")
ax.set_xlabel("Licensed Social Workers")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Images/LicensedSocialWorkersandPsychiatrists.png")


#%% TWO PANEL GRAPH FOR SCATTERPLOT COMPARISONS

# set up a figure with two axis
fig1, (ax1,ax2) = plt.subplots(1,2, sharey=True)
fig1.suptitle("Psychiatrists Correlation")

# set up first pane graph- create variable for x and y bar
youth_MHS.plot.scatter(ax=ax1, x="Pediatricians", y="Psychiatrists")
ax1.set_xlabel("Pediatricians")
ax1.set_ylabel("Psychiatrists")

# set up second pane graph- create variable for x and y bar
youth_MHS.plot.scatter(ax=ax2, x="Licensed Social Workers", y="Psychiatrists")
ax2.set_xlabel("Licensed Social Workers")
ax2.set_ylabel("Psychiatrists")
fig1.tight_layout()
fig1.savefig("Images/TwoPanelComparison.png")

#%% TOTAL POPULATION COMPARISONS
# for all total population comparisons we use data found in the cenus

#%% Total Population and Psychiatrists

# create scatter plot across Total Population & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Psychiatrists', ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
# sns.lmplot(x= 'TOTAL_POP', y='Psychiatrists', data=youth_MHS)
# sns.lmplot(x= 'FAM_INCOME', y='Psychiatrists', data=youth_MHS)

# save image of total population and Psychiatrists
ax.set_title("Total Population Psychiatrists NYS Counties")
ax.set_xlabel("Total Population")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Images/TotalPopulationPsychiatrists-NYSCounties.png")

#%% Total Population and Licensed Social Workers

# create scatter plot across Total Population & Licensed Social Workers
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Licensed Social Workers', ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
# sns.lmplot(x= 'TOTAL_POP', y='Licensed Social Workers', data=youth_MHS)
# sns.lmplot(x= 'FAM_INCOME', y='Licensed Social Workers', data=youth_MHS)

# save image of total population and Psychiatrists
ax.set_title("Total Population LSW NYS Counties")
ax.set_xlabel("Total Population")
ax.set_ylabel("Licensed Social Workers")
fig.tight_layout()
fig.savefig("Images/TotalPopulationSocialWorkers-NYSCounties.png")


#%% FAMILY INCOME INCLUDED- SEABORN RELPLOTS
# for family income graphs we use data found in the cenus

# Seaborn plots (set up)

# The sizes argument sets the minimum and maximum sizes that will be used
# for points (which are scaled by the population of each ring). 
# The facet_kws argument is a dictionary of tweaks allowed by Seaborn's 
# FacetGrid objects: the 'despine' argument says not to remove the top 
# and right borders of the graph, and the subplot_kws is a dictionary of 
# tweaks that are passed on to the underlying matplotlib routines (here 
# it just adds a title). 


#%% Family Income and Psychiatrists

fg = sns.relplot(data= youth_MHS, x='FAM_INCOME', y= 'Psychiatrists',
                 size='POP', sizes=(10,200),
                 facet_kws={'despine': False, 
                            'subplot_kws': {'title': 'Family Income vs Psychiatrists'}})
fg.savefig("Images/FamilyIncomebyPsychiatrists.png")

#%% Family Income and Pediatricians

fg = sns.relplot(data= youth_MHS, x='FAM_INCOME', y= 'Pediatricians',
                 size='POP', sizes=(10,200),
                 facet_kws={'despine': False, 
                            'subplot_kws': {'title': 'Family Income vs Pediatricians'}})
fg.savefig("Images/FamilyIncomebyPediatricians.png")

#%% Family Income and Licensed Social Workers

fg = sns.relplot(data= youth_MHS, x='FAM_INCOME', y= 'Licensed Social Workers',
                 size='POP', sizes=(10,200),
                 facet_kws={'despine': False, 
                            'subplot_kws': {'title': 'Family Income vs Licensed Social Workers'}})
fg.savefig("Images/FamilyIncomebyLSW.png")

#%% Family Income and Psychologists

fg = sns.relplot(data= youth_MHS, x='FAM_INCOME', y= 'Psychologists',
                 size='POP', sizes=(10,200),
                 facet_kws={'despine': False, 
                            'subplot_kws': {'title': 'Family Income vs Psychologists'}})
fg.savefig("Images/FamilyIncomebvPsychologists.png")

#%% Family Income four panel comparison

youth_trim = youth_MHS.set_index(["FAM_INCOME", "POP", "County"])
youth_trim = youth_trim[["Psychiatrists",
                         "Pediatricians", 
                         "Licensed Social Workers", 
                         "Psychologists"]]
youth_stack = youth_trim.stack()

youth_stack= youth_stack.reset_index()
youth_stack = youth_stack.rename(columns= {"level_3":"Provider", 0:"Rate"})

fg = sns.relplot(data= youth_stack, x='FAM_INCOME', y= 'Rate', col="Provider",
                 size='POP', sizes=(10,200), col_wrap=2,
                 facet_kws={'despine': False,})
fg.figure.suptitle("Side-by-Side Family Income across providers")
fg.tight_layout()
fg.savefig("Images/SidebySideFamilyIncomeacrossproviders.png")


#%% HEX PLOT
# produces high-level graphics object that doesn't require the subplot function

#%% Licensed Social Workers and Psychiatrists

jg = sns.jointplot( data=youth_MHS, x="Licensed Social Workers", y="Psychiatrists",
                   kind= "hex")

# save image of hex plot
jg.set_axis_labels("Licensed Social Workers", "Psychiatrists")
jg.fig.suptitle("LSW & Psychiatrists")
jg.fig.tight_layout()
jg.savefig("Images/Licensed Social WorkersandPsychiatristsHex.png")

#%% DENSITY OF PROBABILITY PLOT- All PROVIDERS

# stack data to create overlapping densities of different types of doctors availible
# this displays the likleyhood of finding a specific provider within each county
stacked = youth_MHS [['County', 'Pediatricians',
                      'Psychiatrists', 'Family Medicine Physicians',
                      'Licensed Social Workers','Psychologists']]
stacked = stacked.set_index("County")
stacked = stacked.stack().reset_index()
stacked = stacked.rename(columns= {"level_1": "Provider", 0:"Count"})

# saving the image of density plot
fig,ax = plt.subplots()
sns.kdeplot(data=stacked, x="Count", hue= "Provider", fill=True, ax=ax)
ax.set_title("Probability Density Multiple Providers")
fig.tight_layout()
fig.savefig("Images/ProbabilityDensityAllProviders.png")
