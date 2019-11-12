__author__ = 'Andres Perez Dominguez'

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from tkinter import messagebox
import os
from tkinter import *


def get_news_schema():
    return Schema(category=TEXT(stored=True), title=TEXT(stored=True),
                  link=TEXT(stored=True), description=TEXT,
                  date=DATETIME(stored=True))



def create_news_index(dir_index, news):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_news_schema())
    writer = ind.writer()

    for story in news:
        category = story[0]
        title = story[1]
        link = story[2]
        description = story[3]
        date = story[4]
        writer.add_document(category=category, title=title, link=link, description=description, date=date)

    writer.commit()
    messagebox.showinfo("Terminado",
                        "Base de datos creada correctamente. Se han guardado " + str(len(news)) + " noticias")


def search_news_a(text):
    ix = open_dir("news_index")

    words = text.split(" ")
    for word in words:
        text += " description:" + word

    with ix.searcher() as searcher:
        my_query = QueryParser("title", ix.schema).parse(text)

        results = searcher.search(my_query, limit=None)
        news = [[r["category"], r["title"], r["date"]] for r in results]

    return news


def get_yyyymmdd(date):
    splitted_date = date.split("/")
    return splitted_date[2] + splitted_date[1] + splitted_date[0]


def search_news_b(from_date, to_date):
    ix = open_dir("news_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("date", ix.schema).parse(
            "date:[" + get_yyyymmdd(from_date) + " to " + get_yyyymmdd(to_date) + "]")
        results = searcher.search(my_query, limit=None)
        news = [[r["title"], r["date"]] for r in results]

    return news


def search_news_c(sentence):
    ix = open_dir("news_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("description", ix.schema).parse("\"" + sentence + "\"")

        results = searcher.search(my_query, limit=None)
        news = [[r["category"], r["title"], r["date"]] for r in results]

    return news

def extract_news_from_pages(number_of_pages):
    res = []
    for n in range(number_of_pages):
        res.extend(extract_news("http://www.sensacine.com/noticias/?page=" + str(n + 1)))
    return res

def show_news_c(news, frame):
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    my_list = Listbox(frame, yscrollcommand=scrollbar.set)
    my_list.pack(fill=BOTH, expand=1)
    scrollbar.config(command=my_list.yview)
    # Add elements to listbox
    if news is not None:
        for item in news:
            my_list.insert(END, "Title: " + item[0])
            my_list.insert(END, "Link image: " + str(item[1]))
            my_list.insert(END, "Description: " + str(item[2]))
            my_list.insert(END, "")


def show_news_b(news, frame):
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    my_list = Listbox(frame, yscrollcommand=scrollbar.set)
    my_list.pack(fill=BOTH, expand=1)
    scrollbar.config(command=my_list.yview)
    # Add elements to listbox
    if news is not None:
        for item in news:
            my_list.insert(END, "Title: " + item[0])
            my_list.insert(END, "Date: " + str(item[1]))
            my_list.insert(END, "")


def show_news_a(news, frame):
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    my_list = Listbox(frame, yscrollcommand=scrollbar.set)
    my_list.pack(fill=BOTH, expand=1)
    scrollbar.config(command=my_list.yview)
    # Add elements to listbox
    if news is not None:
        for item in news:
            my_list.insert(END, "Category " + item[0])
            my_list.insert(END, "Title: " + item[1])
            my_list.insert(END, "Date: " + str(item[2]))
            my_list.insert(END, "")


def search_window(option):
    new_window = Toplevel()
    new_window.title("Search")
    new_window.geometry("800x600")

    main_frame = Frame(new_window)
    results_frame = Frame(new_window)
    main_frame.pack()
    results_frame.pack(fill=BOTH, expand=1)

    entry = Entry(main_frame)
    entry.pack(side="left")

    if option == 1:
        def search_caller():
            clear_window(results_frame)
            # news = search_news_a(entry.get())
            news = [["Categoria", "Titulo", "Fecha"], ["Categoria1", "Titulo1", "Fecha1"]]
            show_news_a(news, results_frame)
    elif option == 2:
        def search_caller():
            clear_window(results_frame)
            # news = search_news_b(entry.get())
            news = [["Titulo", "Fecha"], ["Titulo1", "Fecha1"]]
            show_news_b(news, results_frame)
    else:
        def search_caller():
            clear_window(results_frame)
            # news = search_news_c(entry.get())
            news = [["Titulo", "Link", "Descripcion"], [ "Titulo1", "Link2", "Descripcion3"]]
            show_news_c(news, results_frame)

    b = Button(main_frame, text="Search", command=search_caller)
    b.pack(side="right")


def clear_window(tk):
    ls = tk.pack_slaves()
    for l in ls:
        l.destroy()


def main():
    root = Tk()

    def close_window():
        root.destroy()

    root.title("Sensacine")
    root.geometry("800x600")

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Home
    home_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Home", menu=home_menu)

    home_menu.add_command(label="Create index", command=lambda: create_news_index(extract_news_from_pages(3)))
    home_menu.add_separator()
    home_menu.add_command(label="Close", command=close_window)

    search_menu = Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="Search", menu=search_menu)

    search_menu.add_command(label="By title and description", command=lambda: search_window(1))
    search_menu.add_command(label="By date", command=lambda: search_window(2))
    search_menu.add_command(label="By description", command=lambda: search_window(3))

    root.mainloop()


if __name__ == '__main__':
    print(translate('12 de noviembre de 2019'))
    main()
