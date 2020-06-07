# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:49:15 2020

@author: mpenm
"""
'''
Output lists : 

all_links - contains all the links with titles 
linkswithlocations - contains gofundme links with title, organizer name, city details

to access each link, put in a loop and get one by one : linkswithlocations[n]

'''

import requests
from bs4 import BeautifulSoup

global datamain
all_links =[]
invalidlinks = []
linkswithlocations = []
gofundmelinks =[]

placestoscrape = ['petitions','more','victims','bail','business','org','other','resources']  #list of pages to sctrape within the website


def start_scrape(page):
    link = 'https://blacklivesmatters.carrd.co/#' + page                  # page is a string that has link end extension
    sectionid = page + '-section'
    req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.content,"html5lib")
     
    table = soup.find('section', attrs = {'id': sectionid})#section id - html element to look for when scraping
      
    for row in table.findAll('ul', attrs = {'class':'buttons'}): 
        data = {} 
        data['title'] = row.find('a').contents[0]
        data['url'] = row.a['href'] 
        all_links.append(data)     
    return all_links                # list containing the data

# runs the scraping script
def scrape_eachlink(link):
    
    req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.content,"html5lib")
     
    table = soup.find('div', attrs = {'class': 'm-campaign-members-main-organizer'})#section id - html element to look for when scraping
    table1 = soup.find('header', attrs = {'class': 'p-campaign-header'})  
    for hd in table1.findAll('h1', attrs = {'class':'a-campaign-title'}):
        loc = {}
        loc['title'] = hd.contents[0]      
        for row in table.findAll('div', attrs = {'class':'m-person-info-content'}):
            loc['link'] = link
            loc['city'] = row.findAll('div', attrs = {'class':'text-small'})[-1].contents[0]
            for nm in table.findAll('div', attrs = {'class':'m-person-info-name'}):
                loc['organizer_name'] = nm.contents[0]
            linkswithlocations.append(loc)  
    return linkswithlocations


for sec in placestoscrape:
    start_scrape(sec)

# gets the links that are invalid (starting with #)    
for i in range(len(all_links)):
    urlstr = all_links[i]['url']
    substr = all_links[i]['url'][0]
    if substr == '#':
        invalidlinks.append(i)
        
# Removes the unwanted links from data link list

l = 0
for j in invalidlinks:
    del all_links[j-l]
    l = l+1
        
for k in range(len(all_links)):
    linkstr = all_links[k]['url']
    linksubstr = all_links[k]['url'][12:20]
    if linksubstr == 'gofundme':
        gofundmelinks.append(linkstr)    
        

for glink in gofundmelinks:
    scrape_eachlink(glink)    

