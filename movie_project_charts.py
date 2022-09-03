# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 13:34:03 2021

@author: nicho
"""


import pandas as pd

df = pd.read_csv("results_21.csv")

df_save = df.copy()


### Cleaning the data
df = df.reset_index(drop=True)

for x in range(0,len(df)):
    try:
        int(df['Metascore Pro Rating'][x])
        float(df['Public Average Rating (IMDb)'][x])
        if df['Metascore Name (check for validity)'][x] == df['IMBd title (check for validity)'][x]:
            pass
        else:
            df = df.drop([x])                
    except:
        df = df.drop([x])
        pass


    

#Getting the numbers ready to regress
df['Public Average Rating (IMDb)'] = pd.to_numeric(df['Public Average Rating (IMDb)'], downcast="float")
df['Public Average Rating (IMDb)'] = df['Public Average Rating (IMDb)']*10

df = df.reset_index(drop = True)

for x in range(0,len(df)):
    try:
        if 'K' in df['Number Public Votes (IMDb)'][x]:
            df['Number Public Votes (IMDb)'][x] = df['Number Public Votes (IMDb)'][x].replace('K','')
            df['Number Public Votes (IMDb)'][x] = pd.to_numeric(df['Number Public Votes (IMDb)'][x])
            df['Number Public Votes (IMDb)'][x] = df['Number Public Votes (IMDb)'][x]*1000
        elif 'M' in df['Number Public Votes (IMDb)'][x]:
            df['Number Public Votes (IMDb)'][x] = df['Number Public Votes (IMDb)'][x].replace('M','')
            df['Number Public Votes (IMDb)'][x] = pd.to_numeric(df['Number Public Votes (IMDb)'][x])
            df['Number Public Votes (IMDb)'][x] = df['Number Public Votes (IMDb)'][x]*1000000
    except:
        pass






#Create dummy variables
for x in range(0,len(df)):
    df['race_ethnicity'][x] = df['race_ethnicity'][x].replace(' ','')
    df['religion'][x] = df['religion'][x].replace(' ','')
    df['sexual_orientation'][x] = df['sexual_orientation'][x].replace(' ','')

df = pd.get_dummies(df, columns=['race_ethnicity'])
df = pd.get_dummies(df, columns=['religion'])
df = pd.get_dummies(df, columns=['sexual_orientation'])

df['religion_Anglican'] = df['religion_Anglican/episcopalian']
df['religion_Born_AgainChristian'] = df['religion_Born-AgainChristian']


df['number_public_votes'] = pd.to_numeric(df['Number Public Votes (IMDb)'])

df['pro_rating'] = pd.to_numeric(df['Metascore Pro Rating'])
df['number_professional_votes'] = pd.to_numeric(df['Number of Professional Reviewers'])
df['public_rating'] = pd.to_numeric(df['Public Average Rating (IMDb)'])


#Public minus critic variable
df['Metascore Pro Rating'] = pd.to_numeric(df['Metascore Pro Rating'])
df['public_minus_critic'] = df['Public Average Rating (IMDb)'] - df['Metascore Pro Rating']

#Year variable made from year of award
df['year'] = 0
for x in range(0,len(df)):
    df['year'][x] = df['year_of_award'][x] - df['year_of_award'].min()




df = df[['public_minus_critic','pro_rating','public_rating', 'number_public_votes', 'number_professional_votes', 'year', 'race_ethnicity_Asian', 'race_ethnicity_Black', 'race_ethnicity_Hispanic','race_ethnicity_MiddleEastern' ,'race_ethnicity_Multiracial','religion_Agnostic' ,'religion_Anglican','religion_Atheist','religion_Baptist','religion_Born_AgainChristian','religion_Buddhist','religion_ChristianScience','religion_Congregationalist','religion_Deist','religion_DisciplesofChrist','religion_Hindu','religion_Jewish','religion_Lutheran','religion_Na','religion_Presbyterian','religion_Protestant','religion_Quaker','religion_RomanCatholic','religion_SeeNote','sexual_orientation_Bisexual','sexual_orientation_Gay','sexual_orientation_Lesbian','sexual_orientation_MatterofDispute','sexual_orientation_Na']]
#' + ', data=df)
#]]

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

corr = df.corr(method='pearson')

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(7, 6))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True, sep=100)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0, linewidths=.5)

fig.suptitle('Correlation matrix of features', fontsize=15)
#ax.text(0.77, 0.2, 'aegis4048.github.io', fontsize=13, ha='center', va='center',
#         transform=ax.transAxes, color='grey', alpha=0.5)

fig.tight_layout()





import statsmodels.formula.api as smf

#Control groups
#race_ethnicity_White
#religion_Christian
#sexual_orientation_Straight

#Do identity characteristics coorelate with a difference between normal individuals ratings and professional ratings?
mod = smf.ols('public_minus_critic ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + religion_SeeNote + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res = mod.fit()
print(res.summary())


import statsmodels.api as sm


fig = sm.graphics.influence_plot(res, criterion="cooks")
fig.tight_layout(pad=1.0)

f = open('public_minus_critic.txt', 'w')
f.write(str(res.summary()))
f.close()















#Do identity characteristics impact the number of public votes a movie recieves?
mod = smf.ols('number_public_votes ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + religion_SeeNote + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res = mod.fit()
print(res.summary())

f = open('number_public_votes.txt', 'w')
f.write(str(res.summary()))
f.close()





#Do identity characteristics impact the number of professional votes a movie recieves?
mod = smf.ols('number_professional_votes ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + religion_SeeNote + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res = mod.fit()
print(res.summary())


f = open('number_professional_votes.txt', 'w')
f.write(str(res.summary()))
f.close()


#Do identity characteristics impact the professional reviews?
mod = smf.ols('pro_rating ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + religion_SeeNote + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res = mod.fit()
print(res.summary())

f = open('pro_rating.txt', 'w')
f.write(str(res.summary()))
f.close()

#Do identity characteristics impact the regular reviews?
mod = smf.ols('public_rating ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + religion_SeeNote + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res = mod.fit()
print(res.summary())

f = open('public_rating.txt', 'w')
f.write(str(res.summary()))
f.close()











df.to_csv("results_cleaned.csv")




































