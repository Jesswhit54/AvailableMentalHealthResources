# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 17:21:00 2023

@author: jessi
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.dpi'] = 300
import youth_MHS as youth_MHS

# GRAPHING AND PLOTTING DATA
# various data visualization  methods can be seen below


#%% SCATTER PLOTS AND REGRESSIONS

# create scatter plot across Pediatricians & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'Pediatricians', y='Psychiatrists',ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
sns.lmplot(x= 'Pediatricians', y='Psychiatrists', data=youth_MHS)

ax.set_title( "Pediatricians & Psychiatrists")
ax.set_xlabel("Pediatricians")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Pediatricians & Psychiatrists.png")

#%%

# create scatter plot across Total Population & Psychiatrists
fig,ax = plt.subplots()
youth_MHS.plot.scatter(x= 'TOTAL_POP', y= 'Psychiatrists', ax=ax)

# run a regression on the scatterplot with a 95% confidence interval
#sns.lmplot(x= 'TOTAL_POP', y='Psychiatrists', data=youth_MHS)

ax.set_title("Total Population of NYS Counties")
ax.set_xlabel("Total Population")
ax.set_ylabel("Psychiatrists")
fig.tight_layout()
fig.savefig("Total Population of NYS Counties")

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
ax.set_title("Probability Desnity Multiple Providers")
fig.tight_layout()
fig.savefig("Probability Density Multiple Providers")



