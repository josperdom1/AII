import sqlite3
import urllib.request
from datetime import datetime
from tkinter import *
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
        if len(film) >= 6:
            cat2 = film[5]
        if len(film) == 7:
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
    cur.execute("SELECT * FROM FILM WHERE PUBLISH_DATE > '" + date + "'")
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


def close_window(tk):
    tk.destroy()


def show_films(tk, films):
    scrollbar = Scrollbar(tk)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # Crea la listbox que es un widget
    mylist = Listbox(tk, yscrollcommand=scrollbar.set)
    mylist.pack(fill=BOTH, expand=1)
       
    scrollbar.config(command=mylist.yview)
    
    # Añado los elementos a mi listbox
    for item in films:
        mylist.insert(END, "Title: " + item[0])
        mylist.insert(END, "Link: " + item[1])
        mylist.insert(END, "Publish Date: " + item[2])
        mylist.insert(END, "Country: " + item[3])
        mylist.insert(END, "Categories: " + item[4]) #+", "+item[5]+", "+item[6])
        if item[5] is not None:
            mylist.insert(END, "                  " + item[5])
        if item[6] is not None:
            mylist.insert(END, "                  " + item[6])
        mylist.insert(END, "")


def all_films(tk):
    bdd =  sqlite3.connect('films.db') #insertar nombre BDD
    cursor =  bdd.cursor()
    
    cursor.execute("SELECT *  FROM FILM")
    
    films =  cursor.fetchall()
    
    show_films(tk, films)
    

#Auxiliar Windows

def window_search_date():
    new_window = Toplevel()
    new_window.geometry("300x200")
    new_window.title("Buscar por Fecha")
    
    entry = Entry(new_window, width=10)
    entry.pack(side=LEFT)
    
    def search_caller():
        ls = select_by_date(entry.get())
        
        results_window = Toplevel()
        results_window.geometry("800x600")
        
        show_films(results_window, ls)
    
    button = Button(new_window, text="Buscar", command=search_caller)
    button.pack(side=LEFT)
     
   
def window_search_genre():
    
    new_window = Toplevel()
    new_window.geometry("400x200")
    new_window.title("Buscar por Fecha")

    spinbox = Spinbox(new_window, values=get_categories())
    spinbox.pack(side=LEFT)
    
    def search_caller():
        ls = select_by_category(spinbox.get())
        
        results_window = Toplevel()
        results_window.geometry("800x600")
        
        show_films(results_window, ls)
    
    button = Button(new_window, text="Buscar", command=search_caller)
    button.pack(side=LEFT)


def window_search_country():
    new_window = Toplevel()
    new_window.geometry("300x200")
    new_window.title("Buscar por País")
    
    entry = Entry(new_window, width=10)
    entry.pack(side=LEFT)
    
    def search_caller():
        ls = select_by_country(entry.get())
        
        results_window = Toplevel()
        results_window.geometry("800x600")
        
        show_films(results_window, ls)
    
    button = Button(new_window, text="Buscar", command=search_caller)
    button.pack(side=LEFT)
    
    
def main():
    root = Tk()
    
    def call_close_window():
        close_window(root)

    def m ():
        create_db()
        all_films(root)
        
    root.title("Movies")
    root.geometry("800x600")
    
    menubar = Menu(root)
    root.config(menu=menubar)
    
    #Datos   
    datos_menu = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Datos", menu=datos_menu)
    
    datos_menu.add_command(label="Cargar", command=m)
    datos_menu.add_separator()
    datos_menu.add_command(label="Salir", command=call_close_window) 

    
    #Buscar
    buscar_menu = Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Buscar", menu=buscar_menu)

    buscar_menu.add_command(label="Por fecha", command=window_search_date)

    buscar_menu.add_command(label="Por género",command=window_search_genre) 

    buscar_menu.add_command(label="Por país", command=window_search_country)

    root.mainloop()


if __name__ == '__main__':
    main()