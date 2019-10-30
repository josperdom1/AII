
__author__ = 'Andres Perez Dominguez'
import tkinter as tk
import sqlite3
import urllib.request
from tkinter import *
from datetime import datetime
from tkinter import messagebox
from bs4 import BeautifulSoup


def extract():
    html_doc = urllib.request.urlopen("https://www.elseptimoarte.net/estrenos").read()
    soup = BeautifulSoup(html_doc, "html.parser")

    movies = soup.find("ul", "elements").find_all("li")

    res = []

    for i in movies:

        movie = []

        a = i.find("a")
        title = a.string
        movie.append(str(title))

        link = "https://www.elseptimoarte.net" + a.get("href")
        movie.append(str(link))

        movie_html = urllib.request.urlopen(link).read()
        movie_soup = BeautifulSoup(movie_html, "html.parser")

        publish_date_str = movie_soup.find(text="Estreno en España").parent.next_sibling.next_sibling.string
        publish_date = datetime.strptime(publish_date_str, "%d/%m/%Y").date()
        movie.append(publish_date)

        country = movie_soup.find(text="País").parent.next_sibling.next_sibling.find("a").string
        movie.append(str(country))

        categories = movie_soup.find("p", "categorias")
        for cat in categories.find_all("a"):
            movie.append(str(cat.string))

        res.append(movie)

    return res


def create_db():
    films = extract()

    db = sqlite3.connect('films.db')  # conectando a la base de datos
    cursor = db.cursor()

    cursor.execute("""DROP TABLE IF EXISTS FILM""")
    cursor.execute(
        """CREATE TABLE FILM( TITLE TEXT NOT NULL,
        LINK TEXT NOT NULL,
        PUBLISH_DATE DATE NOT NULL,
        COUNTRY NOT NULL,
        CATEGORY_ONE TEXT,
        CATEGORY_TWO TEXT,
        CATEGORY_THREE TEXT
        )""")

    for film in films:
        cat2 = None
        cat3 = None
        title = film[0]
        link = film[1]
        publish_date = film[2]
        country = film[3]
        cat1 = film[4]
        if len(film)>=6:
            cat2 = film[5]
        if len(film)==7:
            cat3 = film[6]


        cursor.execute("""INSERT INTO FILM 
        (TITLE, LINK, PUBLISH_DATE, COUNTRY, CATEGORY_ONE,  CATEGORY_TWO, CATEGORY_THREE )
         values(?,?,?,?,?,?,?)""",
                       (title, link, publish_date, country, cat1, cat2, cat3))

    db.commit()

    cursor = db.execute("SELECT COUNT(*) FROM FILM")
    messagebox.showinfo("Terminado", "Base de datos creada correctamente. Se han guardado " + str(
        cursor.fetchone()[0]) + " elementos")

    db.close()


def get_categories():
    db = sqlite3.connect('films.db')
    db.text_factory = str
    cursor = db.cursor()

    ls = cursor.execute("SELECT  DISTINCT CATEGORY_ONE, CATEGORY_TWO, CATEGORY_THREE FROM FILM").fetchall()
    print(ls)

    cat = []

    for l in ls:
        for e in l:
            if e is not None and e not in cat:
                cat.append(e)
    return cat


def verBD():
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM FILM")
    print(cur.fetchall())

def select_by_date(date):
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM FILM WHERE PUBLISH_DATE > '" + date + "'" )
    return cur.fetchall()

def select_by_country(country):
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM FILM WHERE COUNTRY = '" + country + "'")
    return cur.fetchall()

def select_by_category(category):
    conn = sqlite3.connect('films.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM FILM WHERE CATEGORY_ONE = '" + category + "' OR CATEGORY_TWO = '" + category + "' OR CATEGORY_THREE = '" + category + "'")
    return cur.fetchall()




create_db()
verBD()
print(select_by_country('USA'))
