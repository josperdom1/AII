from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import re

#Leo la pagina y la guardo en un archivo fichero
pagina = urllib.request.urlretrieve("http://www.us.es/rss/feed/portada","fichero")
#Abro el fichero codificandolo en utf-8 para conseguir texto en lenguaje natural, y lo leo para obtener el codigo fuente en HTML
codigoFuente = open("fichero", "r", encoding='utf-8').read()
# print(codigoFuente)
#A partir del texto plano en HTML creo un objeto soup
soup = BeautifulSoup(codigoFuente)
# print(soup.prettify())
# #prettify sirve para pintar el html que contiene el objeto soup

for i in soup.find_all("item"):
    print(i)
    print(i.find('title').string)
    # print(i.find('title').next_sibling.string)
    print(i.find('pubdate').string)








