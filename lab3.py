__author__ = 'Andrés Perez Domínguez'
import tkinter as tk
import sqlite3
import urllib.request
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter import messagebox
from bs4 import BeautifulSoup

html_doc = urllib.request.urlopen('https://www.meneame.net').read()

soup = BeautifulSoup(html_doc, 'html.parser')
divs = soup.find_all('div', class_="center-content")

for div in divs:
    title = div.find('h2').find('a').string
    link = div.find('h2').find('a').get('href')
    author = div.find('div', class_='news-submitted').find('a').get('href').replace('/user/','')
    date = datetime.fromtimestamp(int(div.find_all('span')[-1].get('data-ts')))
    print(date)



# def extract_threads(url):
#     html_doc = urllib.request.urlopen(url).read()
#
#     soup = BeautifulSoup(html_doc, 'html.parser')
#
#     threadbits = soup.find_all('li', class_="threadbit")
#
#     threads = []
#
#     for t in threadbits:
#         thread = []
#
#         thread_title = t.find("a", "title")
#         thread.append(str(thread_title.string))
#         thread.append(str("https://foros.derecho.com/" + thread_title.get('href')))
#
#         thread_subtitle = t.find("a", class_="username")
#         thread.append(str(thread_subtitle.string))
#         thread.append(str(thread_subtitle.next_sibling.replace(u"\xa0", u" ").replace(", ", "")))
#
#         thread_stats = t.find("ul", class_="threadstats").find_all("li")
#         thread.append(str(thread_stats[0].find("a").string))
#         thread.append(str(thread_stats[1].string.replace("Visitas: ", "")))
#
#         threads.append(thread)
#
#     return threads
#
#
# def extract_threads_from_pages(number_of_pages):
#     res = []
#     for n in range(number_of_pages):
#         res.extend(extract_threads("https://www.meneame.net/?page=" + str(n + 1)))
#     return res

# def create_db():
#     products = extract()
#
#     db = sqlite3.connect('products.db')  # conectando a la base de datos
#     cursor = db.cursor()
#
#     cursor.execute("""DROP TABLE if exists producto""")  # si existe la tabla 'producto' la elimina
#     # creamos la tabla producto: marca, nombre, link a la descripcion del producto y precio/s (si est en oferta tiene de un precio).
#     cursor.execute(
#         """CREATE TABLE producto (marca text not null, nombre text not null, link text not null, precio real not null, oferta real)""")
#
#     for product in products:
#         marca = product[0]
#         nombre = product[1]
#         link = product[2]
#         precio = product[3]
#         oferta = None
#         if len(product) == 5:
#             oferta = product[4]
#
#         cursor.execute("""INSERT INTO producto (marca, nombre, link , precio, oferta) values(?,?,?,?,?)"""
#                        , (marca, nombre, link, precio, oferta))
#
#     db.commit()  # guardar el resultado de las operaciones realizadas en la BDD
#
#     cursor = db.execute("SELECT COUNT(*) FROM PRODUCTO")  # numero de filas guardadas
#     messagebox.showinfo("Terminado", "Base de datos creada correctamente. Se han guardado " + str(
#         cursor.fetchone()[0]) + " elementos")
#
#     db.close()