__author__ = 'Andres Perez Dominguez'

import urllib.request
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
import os
from tkinter import *
from tkinter import messagebox
import urllib
import dateutil.parser
from bs4 import BeautifulSoup
from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
from datetime import datetime as dt


def extract_events():
    html_doc = urllib.request.urlopen(
        "https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades").read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    events = soup.find_all("div", "cal_info")

    saved_events = []

    for e in events:

        event = []

        title = e.find("span", "summary").get_text()

        event.append(str(title))

        document_by_line = e.find("div", "documentByLine")

        try:
            start_date = document_by_line.find("abbr", "dtstart").get("title")
            event.append(dateutil.parser.parse(start_date))
        except:
            try:
                event.append(dt.strptime(document_by_line.contents[0].strip(), "%d/%m/%Y"))
            except:
                event.append(None)

        try:
            end_date = document_by_line.find("abbr", "dtend").get("title")
            event.append(dateutil.parser.parse(end_date))
        except:
            event.append(None)

        try:
            description = e.find("p", "description").string
            event.append(str(description))
        except:
            event.append("")

        categories = []
        li_category = e.find("li", "category")
        if li_category is not None:
            for cat in li_category.find_all('span'):
                categories.append(cat.string)

        event.append(", ".join(categories))

        saved_events.append(event)

    return saved_events

def get_events_schema():
    return Schema(title=TEXT(stored=True), start_date=DATETIME(stored=True),
                  end_date=DATETIME(stored=True), description=TEXT(stored=True),
                  categories=TEXT(stored=True))


def create_events_index(dir_index, events):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_events_schema())
    writer = ind.writer()

    for event in events:
        title = event[0]
        start_date = event[1]
        end_date = event[2]
        description = event[3]
        categories = event[4]
        writer.add_document(title=title, start_date=start_date,
                            end_date=end_date, description=description,
                            categories=categories)

    writer.commit()
    messagebox.showinfo("Terminado", "Base de datos creada correctamente. Se han guardado " + str(len(events)) + " elementos")


def search_events_a(text):
    ix = open_dir("events_index")

    words = text.split(" ")
    for word in words:
        text += " description:" + word

    with ix.searcher() as searcher:
        my_query = QueryParser("title", ix.schema).parse(text)

        results = searcher.search(my_query, limit=None)
        #events = [[r["title"], r["start_date"], r["end_date"]] for r in results]

        events = []
        for r in results:
            event = []

            event.append(r["title"])

            try:
                event.append(r["start_date"])
            except:
                event.append("")

            try:
                event.append(r["end_date"])
            except:
                event.append("")

            events.append(event)


    return events


def search_events_b(date):
    ix = open_dir("events_index")
    html_doc = urllib.request.urlopen(
        "https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades").read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    events = soup.find_all("div", "cal_info")

    saved_events = []

    for e in events:

        event = []

        title = e.find("span", "summary").get_text()

        event.append(str(title))

        document_by_line = e.find("div", "documentByLine")

        try:
            start_date = document_by_line.find("abbr", "dtstart").get("title")
            event.append(dateutil.parser.parse(start_date))
        except:
            event.append(None)

        try:
            end_date = document_by_line.find("abbr", "dtend").get("title")
            event.append(dateutil.parser.parse(end_date))
        except:
            event.append(None)

        try:
            description = e.find("p", "description").string
            event.append(str(description))
        except:
            event.append("")

        categories = []
        li_category = e.find("li", "category")
        if li_category is not None:
            for cat in li_category.find_all('span'):
                categories.append(cat.string)

        event.append(", ".join(categories))

        saved_events.append(event)

    return saved_events


def get_events_schema():
    return Schema(title=TEXT(stored=True), start_date=DATETIME(stored=True),
                  end_date=DATETIME(stored=True), description=TEXT(stored=True),
                  categories=TEXT(stored=True))


def create_events_index(dir_index, events):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_events_schema())
    writer = ind.writer()

    for event in events:
        title = event[0]
        start_date = event[1]
        end_date = event[2]
        description = event[3]
        categories = event[4]
        writer.add_document(title=title, start_date=start_date,
                            end_date=end_date, description=description,
                            categories=categories)

    writer.commit()
    messagebox.showinfo("Terminado",
                        "Base de datos creada correctamente. Se han guardado " + str(len(events)) + " elementos")


def search_events_a(text):
    ix = open_dir("events_index")

    words = text.split(" ")
    for word in words:
        text += " description:" + word

    with ix.searcher() as searcher:
        my_query = QueryParser("title", ix.schema).parse(text)

        results = searcher.search(my_query, limit=None)
        # events = [[r["title"], r["start_date"], r["end_date"]] for r in results]

        events = []
        for r in results:
            event = []

            event.append(r["title"])

            try:
                event.append(r["start_date"])
            except:
                event.append("")

            try:
                event.append(r["end_date"])
            except:
                event.append("")

            events.append(event)

    return events


def search_events_b(date):
    ix = open_dir("events_index")
    with ix.searcher() as searcher:
        my_query = QueryParser("start_date", ix.schema).parse(f"start_date:[to {date}]")
        results = searcher.search(my_query, limit=None)
        # events = [[r["title"], r["start_date"], r["end_date"]] for r in results]

        events = []
        for r in results:
            event = []

            event.append(r["title"])

            try:
                event.append(r["start_date"])
            except:
                event.append("")

            try:
                event.append(r["end_date"])
            except:
                event.append("")

            events.append(event)
    return events


def search_events_c(category):
    ix = open_dir("events_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("categories", ix.schema).parse(f'"{category}"')

        results = searcher.search(my_query, limit=None)
        # events = [[r["title"], r["start_date"], r["end_date"]] for r in results]

        events = []
        for r in results:
            event = []

            event.append(r["title"])

            try:
                event.append(r["start_date"])
            except:
                event.append("")

            try:
                event.append(r["end_date"])
            except:
                event.append("")

            events.append(event)

    return events


def get_categories():
    html_doc = urllib.request.urlopen(
        "https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades").read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    events = soup.find_all("div", "cal_info")
    all_categories = []

    for e in events:

        categories = e.find('li', 'category')
        if categories is not None:
            for cat in categories.find_all('span'):
                if not all_categories.__contains__(cat.string):
                    all_categories.append(cat.string)

    return all_categories


def show_events_a(events, frame):
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    my_list = Listbox(frame, yscrollcommand=scrollbar.set)
    my_list.pack(fill=BOTH, expand=1)
    scrollbar.config(command=my_list.yview)
    # Add elements to listbox
    if events is not None:
        for item in events:
            my_list.insert(END, "Title " + item[0])
            my_list.insert(END, "Start date: " + str(item[1]))
            my_list.insert(END, "End date: " + str(item[2]))
            my_list.insert(END, "")


def search_window(option):
    new_window = Toplevel()
    new_window.title("Search")
    new_window.geometry("800x600")

    main_frame = Frame(new_window)
    results_frame = Frame(new_window)
    main_frame.pack()
    results_frame.pack(fill=BOTH, expand=1)

    # entry = Entry(main_frame)
    # entry.pack(side="left")

    # authors = get_authors()
    # spinbox = Spinbox(frame, values=authors)
    # spinbox.pack(side="left")
    # spinbox.get()

    if option == 1:
        entry = Entry(main_frame)
        entry.pack(side="left")

        def search_caller():
            clear_window(results_frame)
            events = search_events_a(entry.get())
            show_events_a(events, results_frame)
    elif option == 2:
        entry = Entry(main_frame)
        entry.pack(side="left")

        def search_caller():
            clear_window(results_frame)
            convert = dt.strptime(entry.get(), '%d de %B de %Y')
            d = convert.strftime("%Y%m%d")
            events = search_events_b(d)
            show_events_a(events, results_frame)
    else:
        categories = get_categories()
        spinbox = Spinbox(main_frame, values=categories)
        spinbox.pack(side="left")

        def search_caller():
            clear_window(results_frame)
            events = search_events_c(spinbox.get())
            show_events_a(events, results_frame)
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

    root.title("Sevilla")
    root.geometry("800x600")

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Home
    home_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Home", menu=home_menu)

    home_menu.add_command(label="Create index", command=lambda: create_events_index('events_index', extract_events()))
    home_menu.add_separator()
    home_menu.add_command(label="Close", command=close_window)

    search_menu = Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="Search", menu=search_menu)

    search_menu.add_command(label="By title and description", command=lambda: search_window(1))
    search_menu.add_command(label="By date", command=lambda: search_window(2))
    search_menu.add_command(label="By category", command=lambda: search_window(3))

    root.mainloop()


if __name__ == '__main__':
    main()