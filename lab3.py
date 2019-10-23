from tkinter.ttk import Scrollbar

__author__ = 'Andres Perez Dominguez'
import tkinter as tk
import sqlite3
import urllib.request
from tkinter import *
from datetime import datetime
from tkinter import messagebox
from bs4 import BeautifulSoup


def extract(url):
    html_doc = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_doc, 'html.parser')
    divs = soup.find_all('div', class_="center-content")

    news = []

    for div in divs:
        new = []

        title = div.find('h2').find('a').string
        link = div.find('h2').find('a').get('href')
        author = div.find('div', class_='news-submitted').find('a').get('href').replace('/user/', '')
        date = datetime.fromtimestamp(int(div.find_all('span')[-1].get('data-ts')))
        content = div.find('div', class_='news-content').string

        new.append(title)
        new.append(link)
        new.append(author)
        new.append(date)
        new.append(content)

        news.append(new)

    return news


def extract_from_pages(number_of_pages):
    res = []
    for n in range(number_of_pages):
        res.extend(extract("https://www.meneame.net/?page=" + str(n + 1)))
    return res


def create_db():
    news = extract_from_pages(3)

    db = sqlite3.connect('news.db')  # conectando a la base de datos
    cursor = db.cursor()

    cursor.execute("""DROP TABLE IF EXISTS NEW""")
    cursor.execute(
        """CREATE TABLE NEW( TITLE TEXT NOT NULL,
        LINK TEXT NOT NULL,
        AUTHOR TEXT NOT NULL,
        PUBLISH_DATE DATETIME NOT NULL,
        CONTENT TEXT)""")

    for new in news:
        title = new[0]
        link = new[1]
        author = new[2]
        publish_date = new[3]
        content = new[4]

        cursor.execute("""INSERT INTO NEW 
        (TITLE, LINK, AUTHOR, PUBLISH_DATE, CONTENT)
         values(?,?,?,?,?)""",
                       (title, link, author, publish_date, content))

    db.commit()

    cursor = db.execute("SELECT COUNT(*) FROM NEW")
    messagebox.showinfo("Terminado", "Base de datos creada correctamente. Se han guardado " + str(
        cursor.fetchone()[0]) + " elementos")

    db.close()


def show_list(elements, tk):
    # Scrollbar
    scrollbar = Scrollbar(tk)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    mylist = Listbox(tk, yscrollcommand=scrollbar.set)
    mylist.pack(fill=BOTH, expand=1)
    scrollbar.config(command=mylist.yview)
    # Add elements to listbox
    for item in elements:
        mylist.insert(END, "Título: " + item[0])
        mylist.insert(END, "Link: " + item[1])
        mylist.insert(END, "Autor: " + item[2])
        mylist.insert(END, "Fecha de publicación: " + str(item[3]))
        if item[4] is not None:
            mylist.insert(END, "Contenido: " + item[4])
        mylist.insert(END, "")


def show_news():
    new_window = Toplevel()
    new_window.title("News")
    new_window.geometry("800x600")

    db = sqlite3.connect('news.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM NEW")

    news = cursor.fetchall()

    show_list(news, new_window)


def get_authors():
    db = sqlite3.connect('news.db')
    cursor = db.cursor()

    cursor.execute("SELECT AUTHOR FROM NEW")

    tuples = cursor.fetchall()
    authors = [x[0] for x in tuples]

    return authors


def search_by_author():
    new_window = Toplevel()
    new_window.title("Buscar por autor")
    new_window.geometry("800x600")
    frame = Frame(new_window)
    frame.pack()
    authors = get_authors()
    spinbox = Spinbox(frame, values=authors)
    spinbox.pack(side="left")
    results_frame = Frame(new_window)
    results_frame.pack(fill=BOTH, expand=1)

    def search_brand_caller():
        clear_window(results_frame)
        search_news_by_author(spinbox.get(), results_frame)

    b = Button(frame, text="Buscar", command=search_brand_caller)
    b.pack(side="right")


def search_news_by_author(author, tk):
    db = sqlite3.connect('news.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM NEW WHERE AUTHOR = '" + author + "'")
    show_list(cursor.fetchall(), tk)


def show_main_buttons():
    store_products_btn = Button(root, text="Almacenar noticias", command=create_db)
    store_products_btn.pack()

    show_brand_btn = Button(root, text="Mostrar noticias", command=show_news)
    show_brand_btn.pack()

    search_deals_btn = Button(root, text="Búsqueda por autor", command=search_by_author)
    search_deals_btn.pack()


def clear_window(tk):
    ls = tk.pack_slaves()
    for l in ls:
        l.destroy()


if __name__ == '__main__':
    root = Tk()
    root.title("Meneame Scrapper")
    root.geometry("300x150")

    show_main_buttons()

    root.mainloop()
