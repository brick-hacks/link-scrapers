# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:49:15 2020

@author: mpenm
"""


import requests
from bs4 import BeautifulSoup

global datamain
datamain =[]

def start_scrape(page,sectionid):
    link = 'https://blacklivesmatters.carrd.co/#' + page                  # page is a string that has link end extension
    req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.content,"html5lib")
     
    table = soup.find('section', attrs = {'id': sectionid})#section id - html element to look for when scraping
      
    for row in table.findAll('ul', attrs = {'class':'buttons'}): 
        data = {} 
        data['text'] = row.find('a').contents[0]
        data['url'] = row.a['href'] 
        datamain.append(data)     
    return datamain                # list containing the data

start_scrape('petitions','petitions-section') #for main petitions screen
start_scrape('more','more-section') # for more petitions
    
datamain = datamain[:-2] #removed last two elements as they are not urls for petitions. They are just redirect links