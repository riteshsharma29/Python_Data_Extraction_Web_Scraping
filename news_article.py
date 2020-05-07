import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


df = pd.DataFrame()
main_url = 'https://www.nytimes.com'
url = f'{main_url}/section/business'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='collection-highlights-container')
articles =  results.find_all('li')
first_article = articles[0]
article_ref = first_article.a.get('href')
article_url = f'{main_url}{article_ref}'

page = requests.get(article_url)    #Navigating to first article
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='site-content')
article = results.find(id='story')

header = article.find('header')
title = header.h1.text  #headline of article
summary = header.p.text #Summary of article

div_ref = article.find_all('div')
story = ''
for div in div_ref:
    result = False
    result = [data for data in div.attrs.values() if 'StoryBodyCompanionColumn' in data]
    if result:
        story = ' '.join([story, div.text]) #Story of article



email_id = re.findall('[a-z0-9!#$%&*+/=?^_{|}~-]+@{1}\w+\.{1}\w+', story)
websites = re.findall('https?://\w+\.{1}\w+|www.\w+\.{1}\w+', story)
phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', story)


#   Designing for presenting in pandas dataframe
max_len = max(len(email_id), len(websites), len(phone))
if not len(email_id) == max_len: email_id.extend(['']*(max_len-len(email_id)))
if not len(websites) == max_len: websites.extend(['']*(max_len-len(websites)))
if not len(phone) == max_len: phone.extend(['']*(max_len-len(phone)))
df.insert(0, "E-Mail", email_id, True) 
df.insert(1, "Website", websites, True) 
df.insert(2, "Telephone", phone, True)
df = pd.DataFrame({"E-Mail":email_id,"Website":websites,"Telephone":phone})
########################################################################
print(df.head())
