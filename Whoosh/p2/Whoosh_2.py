import whoosh

__author__ = 'Andres Perez Dominguez'
from tkinter import messagebox
from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from datetime import datetime
from tkinter import *
from bs4 import BeautifulSoup
import urllib.request
import os


def extract_threads():
    html_doc = urllib.request.urlopen("https://foros.derecho.com/foro/34-Derecho-Inmobiliario").read()
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
        date_str = thread_subtitle.next_sibling.replace(u"\xa0", u" ").replace(", ", "")
        thread.append(datetime.strptime(date_str, "%d/%m/%Y %H:%M"))

        thread_stats = t.find("ul", class_="threadstats").find_all("li")
        thread.append(int(thread_stats[0].find("a").string))
        thread.append(int(thread_stats[1].string.replace("Visitas: ", "").replace(",", "")))

        threads.append(thread)

    return threads


def extract_replies_from_thread(url):
    url = urllib.parse.quote(url.encode('utf8'), ':/')
    html_doc = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    replies = soup.find_all('li', "postcontainer")

    title = soup.find("span", "threadtitle").find("a").string

    res = []

    for p in replies:
        reply = []

        reply.append(title)
        reply.append(url)

        date = p.find("span", "date")
        date_str = date.contents[0] + date.contents[1].string
        reply.append(datetime.strptime(date_str, "%d/%m/%Y, %H:%M"))

        reply_content = ""
        for s in p.find("blockquote", "postcontent").strings:
            reply_content += s.replace("\n", " ").replace("\r", "").replace("\t", "")

        reply.append(str(reply_content))

        try:
            reply.append(p.find("a", "username").string)
        except:
            reply.append("Guest")

        res.append(reply)

    return res


def extract_all_replies(threads):
    res = []
    for th in threads:
        res.extend(extract_replies_from_thread(th[1]))
    return res


def create_thread_index(dir_index, threads):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ix = create_in(dir_index, schema=get_thread_schema())
    writer = ix.writer()
    for thread in threads:
        writer.add_document(title=str(thread[0]), link=str(thread[1]), author=str(thread[2]),
                            date=thread[3], replys=thread[4], views=thread[5])
    writer.commit()

    messagebox.showinfo("Finished", "Indexes for " + str(len(threads)) + " threads created succesfully")


def create_reply_index(dir_index, replies):

    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ix = create_in(dir_index, schema=get_reply_schema())
    writer = ix.writer()
    for reply in replies:
        writer.add_document(thread_title=str(reply[0]), link=str(reply[1]), date=reply[2],
                            content=str(reply[3]), author=str(reply[4]))
    writer.commit()


def get_thread_schema():
    return Schema(title=whoosh.fields.TEXT(stored=True, phrase=False),
                  link=whoosh.fields.TEXT(phrase=False),
                  author=whoosh.fields.TEXT(stored=True, phrase=False),
                  date=whoosh.fields.DATETIME(stored=True),
                  replys=whoosh.fields.NUMERIC, views=whoosh.fields.NUMERIC)


def get_reply_schema():
    return Schema(thread_title=whoosh.fields.TEXT(stored=True, phrase=False),
                  link=whoosh.fields.TEXT(phrase=False),
                  date=whoosh.fields.DATETIME(stored=True),
                  content=whoosh.fields.TEXT, author=whoosh.fields.TEXT(stored=True, phrase=False))


def search_threads_by_title(title):
    ix = open_dir("Thread_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("title", ix.schema).parse(title)
        results = searcher.search(my_query, limit=None)
        threads = []
        for r in results:
            thread = [r['title'], r['author'], r['date']]
            threads.append(thread)

    return threads


def search_threads_by_author(author):
    ix = open_dir("Thread_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("author", ix.schema).parse(author)
        results = searcher.search(my_query, limit=None)
        threads = []
        for r in results:
            thread = [r['title'], r['author'], r['date']]
            threads.append(thread)

    return threads


def search_replies_by_content(query):
    ix = open_dir("Reply_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(my_query, limit=None)
        replies = []
        for r in results:
            reply = [r['thread_title'], r['author'], r['date']]
            replies.append(reply)

    return replies


def show_threads(threads, frame):
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    my_list = Listbox(frame, yscrollcommand=scrollbar.set)
    my_list.pack(fill=BOTH, expand=1)
    scrollbar.config(command=my_list.yview)
    # Add elements to listbox
    if threads is not None:
        for item in threads:
            my_list.insert(END, "Title: " + item[0])
            my_list.insert(END, "Author: " + item[1])
            my_list.insert(END, "Date: " + str(item[2]))
            my_list.insert(END, "")


def show_replies(replies, frame):
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    my_list = Listbox(frame, yscrollcommand=scrollbar.set)
    my_list.pack(fill=BOTH, expand=1)
    scrollbar.config(command=my_list.yview)
    # Add elements to listbox
    if replies is not None:
        for item in replies:
            my_list.insert(END, "Thread title: " + item[0])
            my_list.insert(END, "Author: " + item[1])
            my_list.insert(END, "Date: " + str(item[2]))
            my_list.insert(END, "")


def search_thread_title_window():
    new_window = Toplevel()
    new_window.title("Title search")
    new_window.geometry("800x600")

    main_frame = Frame(new_window)
    results_frame = Frame(new_window)
    main_frame.pack()
    results_frame.pack(fill=BOTH, expand=1)

    entry = Entry(main_frame)
    entry.pack(side="left")

    def search_caller():
        clear_window(results_frame)
        threads = search_threads_by_title(entry.get())
        show_threads(threads, results_frame)

    b = Button(main_frame, text="Search", command=search_caller)
    b.pack(side="right")


def search_thread_author_window():
    new_window = Toplevel()
    new_window.title("Author search")
    new_window.geometry("800x600")

    main_frame = Frame(new_window)
    results_frame = Frame(new_window)
    main_frame.pack()
    results_frame.pack(fill=BOTH, expand=1)

    entry = Entry(main_frame)
    entry.pack(side="left")

    def search_caller():
        clear_window(results_frame)
        threads = search_threads_by_author(entry.get())
        show_threads(threads, results_frame)

    b = Button(main_frame, text="Search", command=search_caller)
    b.pack(side="right")


def search_replies_window():
    new_window = Toplevel()
    new_window.title("Search replies")
    new_window.geometry("800x600")

    main_frame = Frame(new_window)
    results_frame = Frame(new_window)
    main_frame.pack()
    results_frame.pack(fill=BOTH, expand=1)

    entry = Entry(main_frame)
    entry.pack(side="left")

    def search_caller():
        clear_window(results_frame)
        replies = search_replies_by_content(entry.get())
        show_replies(replies, results_frame)

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

    def create_index():
        threads = extract_threads()
        replies = extract_all_replies(threads)
        create_reply_index("Reply_index", replies)
        create_thread_index("Thread_index", threads)


    root.title("Derecho Civil")
    root.geometry("800x600")

    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    #Home
    home_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Home", menu=home_menu)

    home_menu.add_command(label="Create index", command=create_index)
    home_menu.add_separator()
    home_menu.add_command(label="Close", command=close_window)

    #Search
    search_menu = Menu(menu_bar, tearoff=0)
    threads_menu = Menu(search_menu, tearoff=0)

    menu_bar.add_cascade(label="Search", menu=search_menu)
    search_menu.add_cascade(label='Threads', menu=threads_menu)

    threads_menu.add_command(label="By title", command=search_thread_title_window)
    threads_menu.add_command(label="By author", command=search_thread_author_window)
    search_menu.add_command(label="Replies", command=search_replies_window)

    root.mainloop()


if __name__ == '__main__':
    main()


