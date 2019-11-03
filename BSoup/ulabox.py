import sqlite3
from tkinter import *
from tkinter import messagebox
import urllib.request
from bs4 import BeautifulSoup

html_doc = urllib.request.urlopen("https://www.ulabox.com/campaign/productos-sin-gluten#gref").read()

soup = BeautifulSoup(html_doc, 'html.parser')

articles = soup.find_all('article')

for article in articles:
    hgroup = article.find('hgroup', class_='product-item__title')
    brand = hgroup.find('h4').find('a').string
    name = hgroup.find('h3').find('a').string
    price = article.find('strong', class_='product-item__price').find('span', class_='delta').string + article.find('strong', class_='product-item__price').find('span', class_='milli').string
    final_price = float(price[0:3].replace(',','.'))


print(final_price)