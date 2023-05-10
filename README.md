# **New York State: Youth Mental Health Services**
*Are there gaps in youth mental health services?*

# Summary

This is a description of various health resources available for youth in New York State on a county level. The focus of this data is to accesss mental health resources available for youth specifically under the age of 18. The goal is to note any gaps in availible resources for youth. The methods used to access resources can be applied across states. The results can allow for capacity building measures in under served areas. Additionally, youth and educational policy makers can use this data when designing those policies. When creating policy or programs aimed at youth, it is useful to access the capacity of youth and their supports to engage with the implemented programs.

# Input Data

Data for provider information was found on the Center for Disease Control website. [[*Behavioral Health Services in New York, 2015*](https://www.cdc.gov/childrensmentalhealth/stateprofiles-providers/new-york/index.html)]. This data was scrapped from  the CDC webpage and exported to a CSV file. Census data is collected via an API call to pull in relevant variables such as total population, under 18 population and median family income. 

 **mental_health_2015** is our main input displaying the number of behavioral health services by county in New York State, per 10,000 (ten thousand) kids. 
 
    Categories include: 
        pediatricians, 
        family medicine physicians, 
        psychiatrists, 
        psychologists, and 
        licensed social workers.


# Running Script

### *Data_Collection_Under18_Mental_Health_Services.py*
Import and clean data, merge data with left join creating one dataframe with all variables to vizualize and analyze data. 

**A**. Import CSV file 'Behavioral health service providers by county 2015.csv' from the CDC webpage into dataframe **'mental_health_2015'**. 

**B.** Access Census Information

1. Create API to access census information from 2015, input your requested census key to access tables. 

2. Collect relevant census variables, in this case [`Total Population`] , [`Under 18 Population`] and [`Family Income`] and placed into **census_2015** dataframe. 

3. Change 'census_2015' dataframe column names to match the 'mental_health_2015' and drop unnecessary columns. 

4. Merge dataframes in left hand join to ensure no data is lost. 

5. From this point, the user is able to import relevant variables and try different ratios for whatever analysis you would like to run.

        * In this case there is a ratio of 'total population' divided by 10,000 to access the relationship between providers and youth populations.
       ** Manhattan is dropped as an outlyer, as it does not reflect the average we are seeking to access in this project.  

6. Save data to a pickle file in or

### *Displaying-Data.py*








## Whats the take away? Here is the conclusion. run the risk of lacking 

