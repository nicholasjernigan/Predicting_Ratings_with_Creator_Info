# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 11:22:12 2021

Goal: Gather rating information from professionals and regular individuals from the web on a preppared list of shows and movies.

Steps:
1. Copied list of favorite shows from https://ew.com/article/2014/11/03/republican-democrats-favorite-tv-shows/ into excel
2. Split cells to delete the network it is in
3. Load list as df, webscrape metacritic for all professional reviews of the show, put into spreadsheet
4. Get a general rating of the show from normal people (imbd seems good?)





Potential future options: scrape individual reviews for different pros
@author: nicho
"""




import time
#Logic: looks for signs playing 1.2.5 and are enabled that have more than 1000 seconds from responding, and resets them
#Potential problems: reset too many times? Is enabled necessary?



import pandas as pd

#Need selenium to click on the button

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import re



#List of movies you need the information for
df = pd.read_csv("Oscars-demographics-DFE.csv", encoding="ISO-8859-1")

df['Show'] = df['movie']


ms_pr = [] #Meta score pro rating
ms_pn = [] #Meta score pro number
ms_jr = [] #Meta score joe rating
ms_jn = [] #Meta score pro number
ms_name = []





### Metacritic to get pro ratings


###########################################
### Need to change the driver for chrome here:
###########################################
driver_path = r'C:\Users\nicho\Downloads\chromedriver.exe'
driver = webdriver.Chrome(executable_path = driver_path)
url = 'https://www.metacritic.com/tv/the-colbert-report/critic-reviews?sort-by=date&num_items=100'
driver.get(url)

jed=0 
#df['Show']
#for show in df['Show']:
    
##########################Loops through each show in the dataframe 
for x in range(0, len(df)):    
    #show = df['Show'][3]
    show = df['Show'][x]
    
    show = show.lower()
    url_txt = str(show).replace(" ", "-")
    
    urle = "https://www.metacritic.com/movie/" + url_txt
    
    try:
        driver.get(urle)
    except TimeoutException:
        
        time.sleep(3)
        driver.get(urle)    
    driver.get(urle)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,'lxml')
    vare = soup.find_all("td", {'class':"summary_right"})    
    try:
        ms_pr.append(int(re.findall('\d*\.?\d+',vare[0].text)[0]))
    except:
        ms_pr.append('None')        
    try:
        ms_jr.append(float(re.findall('\d*\.?\d+',vare[1].text)[0]))
    except:
        ms_jr.append('None')
    
    
    
    vare = soup.find_all("span", {'class':"based_on"})
    try:
        ms_pn.append(int(re.findall('\d*\.?\d+',vare[0].text)[0]))
    except:
        ms_pn.append('None')     
    try:
        ms_jn.append(float(re.findall('\d*\.?\d+',vare[1].text)[0]))
    except:
        ms_jn.append('None')
        
    vare = soup.find_all("h1")
    try:
        ms_name.append(vare[0].text)
    except:
        ms_name.append('Couldnt pull name')    
    

    
    
    
    
    
    








#IMDb to get Joe ratings

url = 'https://www.imdb.com/title/tt0350448/?ref_=nv_sr_srsg_0'
driver.get(url)


imbd_r = []
imbd_n = []
imbd_name = []
start_date = []

for show in df['Show']:
    
#show = df['Show'][1]

    time.sleep(2)
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="suggestion-search"]').send_keys(show)
    time.sleep(5)
    #Click on first entry
    try:
        driver.find_element_by_xpath('//*[@id="react-autowhatever-1--item-0"]/a').click()
    except:
        imbd_r.append('Not in IMBd')
        imbd_n.append('Not in IMBd')
        imbd_name.append('Not in IMBd')
        start_date.append('Not in IMBd')
        continue
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,'lxml')
    vare = soup.find_all("span", {'class':"AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"})
    try:
        imbd_r.append(float(vare[0].text))
    except:
        imbd_r.append('Not in IMDb')   
    vare = soup.find_all("div", {'class':"AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3 jkCVKJ"})
    try:
        imbd_n.append(vare[0].text)
    except:
        imbd_n.append('Not in IMDb')  
    vare = soup.find_all("span", {'class':"TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex"})    
    if len(vare) > 0:
        start_date.append(vare[0].text)
    else:
        start_date.append('Not Found')
    vare = soup.find_all("h1")    
    imbd_name.append(vare[0].text)













df['Public Average Rating (IMDb)'] = imbd_r
df['Number Public Votes (IMDb)'] = imbd_n
df['IMBd title (check for validity)'] = imbd_name
df['First Air Date'] = start_date
df['Metascore Pro Rating'] = ms_pr
df['Number of Professional Reviewers'] = ms_pn
df['Metascore Name (check for validity)'] = ms_name



df.to_csv("results_21.csv")



### START FROM HERE FOR ANALYSIS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

df = pd.read_csv(r"results_21.csv")



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








df.drop(['religion_SeeNote'], axis=1)


df.to_csv("results_cleaned.csv")



#df = pd.read_csv(r"C:\Users\nicho\Documents\results_cleaned.csv")



import pandas as pd
from sklearn import datasets
import statsmodels.api as sm
from stargazer.stargazer import Stargazer
from IPython.core.display import HTML
import statsmodels.formula.api as smf





#Do identity characteristics coorelate with a difference between normal individuals ratings and professional ratings?
mod = smf.ols('public_minus_critic ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res1 = mod.fit()


#Do identity characteristics impact the number of public votes a movie recieves?
mod = smf.ols('number_public_votes ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res2 = mod.fit()


#Do identity characteristics impact the number of professional votes a movie recieves?
mod = smf.ols('number_professional_votes ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res3 = mod.fit()

#Do identity characteristics impact the professional reviews?
mod = smf.ols('pro_rating ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res4 = mod.fit()

#Do identity characteristics impact the regular reviews?
mod = smf.ols('public_rating ~ year + race_ethnicity_Asian + race_ethnicity_Black + race_ethnicity_Hispanic + race_ethnicity_MiddleEastern + race_ethnicity_Multiracial + religion_Agnostic + religion_Anglican + religion_Atheist + religion_Baptist + religion_Born_AgainChristian + religion_Buddhist + religion_ChristianScience + religion_Congregationalist + religion_Deist + religion_DisciplesofChrist + religion_Hindu + religion_Jewish + religion_Lutheran + religion_Na + religion_Presbyterian + religion_Protestant + religion_Quaker + religion_RomanCatholic + sexual_orientation_Bisexual + sexual_orientation_Gay + sexual_orientation_Lesbian + sexual_orientation_MatterofDispute + sexual_orientation_Na', data=df)
res5 = mod.fit()


#stargazer.render_html()









stargazer = Stargazer([res1, res2])

print(HTML(stargazer.render_html()))



#Stargazer([res1, res2], column.labels=c("default","robust"), align=TRUE)


stargazer = Stargazer([res1, res2, res3, res5, res4])
stargazer.title("Results")

stargazer.custom_columns(['Public Minus Critic', 'Number Public Ratings', 'Number Professional Ratings','Public Rating', 'Professional Rating'], [1, 1,1,1,1])


Html_file= open("filename.html","w")
Html_file.write(stargazer.render_html())
Html_file.close()



#Appendix chart done

#Make simple chart



#Chart with each row being a significant group and each column being what the outcome of interest is
atts = [
'Year' ,
'Asian' ,
'Black' ,
'Hispanic ',
'Middle Eastern' ,
'Multiracial' ,
'Agnostic' ,
'Anglican' ,
'Atheist' ,
'Baptist' ,
'Born Again Christian ',
'Buddhist' ,
'Christian Science' ,
'Congregationalist' ,
'Deist' ,
'Disciples of Christ' ,
'Hindu' ,
'Jewish' ,
'Lutheran' ,
'Religion NA' ,
'Presbyterian' ,
'Protestant' ,
'Quaker' ,
'Roman Catholic' ,
'Bisexual' ,
'Gay' ,
'Lesbian' ,
'Sexual Orientation Disputed' ,
'Sexual Orientation NA']

Pmc = ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O']
numcritic = ['X','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','X','O']
numpro = ['X','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O']
pubrat = ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O']
prorat = ['O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O','O']


tabel = pd.DataFrame(atts)
tabel['Attribute'] = tabel[0]
tabel = tabel[['Attribute']]
tabel['Public Minus Critic Reviews'] = Pmc
tabel['Number Public Reviews'] = numcritic
tabel['Number Professional Reviews'] = numpro
tabel['Public Rating'] = pubrat
tabel['Professional Rating'] = prorat

import plotly.graph_objects as go
import pandas as pd


fig = go.Figure(data=[go.Table(
    header=dict(values=list(tabel.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[tabel['Public Minus Critic Reviews'], tabel['Number Public Reviews'], 
                       tabel['Number Professional Reviews'], tabel['Public Rating'],
                       tabel['Professional Rating']],
               fill_color='lavender',
               align='left'))
])

fig.show()



fig.write_image("yourfile.png") 



import os


os.chdir(r"C:\Users\nicho\Documents\Movie Project")

tabel.to_csv("table.csv")























































































































