#This will not run on online IDE
import requests
import re
from bs4 import BeautifulSoup
import csv


quotes=[]  # a list to store quotes

def ambildata(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'html5lib')
  table = soup.find('ul', attrs = {'class':'cmp_article_list articles'})
  for row in table.findAll("div", attrs = {'class':'obj_article_summary'}):
    quote = {}
    quote['judul'] = re.sub('\s+', ' ', row.h3.text).lstrip().rstrip()
    quote['url'] = row.h3.a['href']
    quote['author'] = row.find("div", attrs = {'class' : 'authors'}).text.lstrip().rstrip()
    detail = row.h3.a['href']
    rd = requests.get(detail)
    sop = BeautifulSoup(rd.content, 'html5lib')
    eek = sop.find('section', attrs = {'class':'item abstract'})
    quote['abstrak'] = eek.find("p").text
    quotes.append(quote)

#ganti link dibawah ini dengan link archive dari jurnal amikom
ambildata("https://jurnal.amikom.ac.id/index.php/infos/issue/view/62")
print(quotes)


filename = "dataset_paper.csv"
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['judul','url','author','abstrak'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)
