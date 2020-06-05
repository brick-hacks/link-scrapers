# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:49:15 2020

@author: mpenm
"""


import requests
from bs4 import BeautifulSoup

global datamain
datamain =[]
invalidlinks = []

placestoscrape = ['petitions','more','victims','bail','business','org','other','resources']  #list of pages to sctrape within the website


def start_scrape(page):
    link = 'https://blacklivesmatters.carrd.co/#' + page                  # page is a string that has link end extension
    sectionid = page + '-section'
    req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.content,"html5lib")
     
    table = soup.find('section', attrs = {'id': sectionid})#section id - html element to look for when scraping
      
    for row in table.findAll('ul', attrs = {'class':'buttons'}): 
        data = {} 
        data['text'] = row.find('a').contents[0]
        data['url'] = row.a['href'] 
        datamain.append(data)     
    return datamain                # list containing the data

# runs the scraping script

for sec in placestoscrape:
    start_scrape(sec)

# gets the links that are invalid (starting with #)    
for i in range(len(datamain)):
    urlstr = datamain[i]['url']
    substr = datamain[i]['url'][0]
    if substr == '#':
        invalidlinks.append(i)
        
# Removes the unwanted links from data link list

l = 0
for j in invalidlinks:
    del datamain[j-l]
    l = l+1
        
    
