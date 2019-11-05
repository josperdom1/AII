__author__ = 'Andrés Perez Domínguez'

import sqlite3
import urllib.request
from tkinter import *
from datetime import datetime
from tkinter import messagebox
from bs4 import BeautifulSoup

def extract_threads_from_pages(number_of_pages):
    res = []
    for n in range(number_of_pages):
        res.extend(extract_threads("https://foros.derecho.com/foro/20-Derecho-Civil-General/page" + str(n + 1)))
    return res

def crearBDDD():
    temas = extract_threads_from_pages(3)
    baseDatos = sqlite3.connect('derechoCivil.db')  # se conecta a la base de datos y no existe la crea
    cursor = baseDatos.cursor()

    cursor.execute("""DROP TABLE if exists tema""")
    # Creamos una tabla con los atributos : título, enlace al tema, autor de inicio del tema, fecha-hora de inicio, respuestas y visitas
    cursor.execute("""CREATE TABLE tema 
    (title text not null, link text not null, author text not null, date_ini datetime not null, answers int not null, visits int not null)""")

    for tema in temas:
        title = tema[0]
        link = tema[1]
        author = tema[2]
        date_ini = datetime.strptime(tema[3], '%d/%m/%Y %H:%M')
        answers = int(tema[4].replace(",", ""))
        visits = int(tema[5].replace(",", ""))
        cursor.execute("""INSERT INTO tema (title, link, author , date_ini, answers, visits) values(?,?,?,?,?,?)"""
                       , (title, link, author, date_ini, answers, visits))

    baseDatos.commit()  # importante guardar el resultado de las operaciones realizadas en la base de datos

    cursor = baseDatos.execute("SELECT COUNT(*) FROM TEMA")  # Número de filas guardadas en la bbdd
    messagebox.showinfo("Terminado", "Base de datos creada correctamente. Se han guardado " + str(
        cursor.fetchone()[0]) + " elementos")
    # fetchone recupera la información de la consulta guardada en el cursor
    # cuando los datos son una colección fetchone recupera el primer elemento y en cada ejecución el siguiente
    baseDatos.close()


def verBD():
    conn = sqlite3.connect('derechoCivil.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM tema")
    print(cur.fetchall())


def extract_threads(url):
    html_doc = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    threadbits = soup.find_all('li', class_="threadbit")

    threads = []

    for t in threadbits:
        thread = []

        thread_title = t.find("a", "title")
        thread.append(str(thread_title.string))
        thread.append(str("https://foros.derecho.com/" + thread_title.get('href')))

        thread_subtitle = t.find("a", class_="username")
        thread.append(str(thread_subtitle.string))
        thread.append(str(thread_subtitle.next_sibling.replace(u"\xa0", u" ").replace(", ", "")))

        thread_stats = t.find("ul", class_="threadstats").find_all("li")
        thread.append(str(thread_stats[0].find("a").string))
        thread.append(str(thread_stats[1].string.replace("Visitas: ", "")))

        threads.append(thread)

    return threads


def mostrar_lista(elementos, tk):
    # Creo la scrollbar
    scrollbar = Scrollbar(tk)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Crea la listbox que es un widget
    mylist = Listbox(tk, yscrollcommand=scrollbar.set)
    mylist.pack(fill=BOTH, expand=1)

    scrollbar.config(command=mylist.yview)
    # Añado los elementos a mi listbox
    for item in elementos:
        mylist.insert(END, "Título: " + item[0])
        mylist.insert(END, "Autor: " + item[1])
        mylist.insert(END, "Fecha: " + item[2])
        mylist.insert(END, "")


def listar_todos(tk):
    baseDatos = sqlite3.connect('derechoCivil.db')
    cursor = baseDatos.cursor()

    cursor.execute("""select title,author,date_ini FROM TEMA""")
    elementos = cursor.fetchall()

    mostrar_lista(elementos, tk)


def listar_mas_populares(tk):
    db = sqlite3.connect('derechoCivil.db')
    cursor = db.cursor()
    cursor.execute("select title,author,date_ini FROM TEMA ORDER BY visits DESC LIMIT 5")
    results = cursor.fetchall()
    mostrar_lista(results, tk)


def listar_mas_activos(tk):
    db = sqlite3.connect('derechoCivil.db')
    cursor = db.cursor()
    cursor.execute("select title,author,date_ini FROM TEMA ORDER BY answers DESC LIMIT 5")
    results = cursor.fetchall()
    mostrar_lista(results, tk)

def buscaTema(tema, tk):
    db = sqlite3.connect('derechoCivil.db')
    cursor = db.cursor()
    cursor.execute("SELECT title,author,date_ini FROM TEMA WHERE title LIKE '%" + tema + "%' ")
    results = cursor.fetchall()
#     clearWindow(tk)
    mostrar_lista(results, tk)
    tk.mainloop()

def addEntry(tk):
    clearWindow(tk)
    frame = Frame(tk)
    frame.pack()
    entry = tk.Entry(frame)
    entry.pack(side="left")
    results_frame = Frame(tk)
    results_frame.pack(fill=BOTH, expand=1)

    def buscador():
        clearWindow(results_frame)
        buscaTema(entry.get(), results_frame)

    b = Button(frame, text="Buscar", command=buscador)
    b.pack(side="right")




def closeWindow(tk):
    tk.destroy()

def clearWindow(tk):
    ls = tk.pack_slaves()
    for l in ls:
        l.destroy()

def mainWindow():
    root = Tk()
    root.geometry("800x600")
    menubar = Menu(root)
    root.config(menu=menubar)

    def llama_listar_todos():
        clearWindow(root)
        listar_todos(root)


    def llama_listar_mas_populares():
        clearWindow(root)
        listar_mas_populares(root)


    def llama_listar_mas_activos():
        clearWindow(root)
        listar_mas_activos(root)

    def close():
        closeWindow(root)

    def buscar():
        addEntry(root)

    # Elemento1
    datosmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Datos", menu=datosmenu)
    datosmenu.add_command(label="Cargar", command=crearBDDD)
    datosmenu.add_command(label="Mostrar", command=llama_listar_todos)
    datosmenu.add_separator()
    datosmenu.add_command(label="Salir", command=close)

    # Elemento2
    buscarmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
    buscarmenu.add_command(label="Tema", command=buscar)
    buscarmenu.add_command(label="Fecha", command=buscar)

    # Elemento3
    estadisticasmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Estadisticas", menu=estadisticasmenu)
    estadisticasmenu.add_command(label="Temas más populares", command=llama_listar_mas_populares)
    estadisticasmenu.add_command(label="Temas más activos", command=llama_listar_mas_activos)

    root.mainloop()




if __name__ == '__main__':

    mainWindow()







