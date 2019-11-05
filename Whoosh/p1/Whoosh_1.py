__author__ = 'Andres Perez Dominguez'

from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from tkinter import messagebox
import os
from tkinter import *
# Crea un indice desde los documentos contenidos en dirdocs
# El indice lo crea en un directorio (dirindex)
def create_index(dir_docs, dir_index):

    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ix = create_in(dir_index, schema=get_schema())
    writer = ix.writer()
    for doc_name in os.listdir(dir_docs):
        if not os.path.isdir(dir_docs + doc_name):
            add_doc(writer, dir_docs, doc_name)
    writer.commit()

    messagebox.showinfo("Finished","Index created succesfully")


def add_doc(writer, path, doc_name):

    file_obj = open(path + '/' + doc_name, "rb")
    from_ = file_obj.readline().strip().decode()
    to_ = file_obj.readline().strip().decode()
    subject_ = file_obj.readline().strip().decode()
    body_ = file_obj.readline().strip().decode()
    file_obj.close()

    writer.add_document(from_who=from_, to_who=to_, subject=subject_, body=body_,
                        id=doc_name)


def get_schema():
    return Schema(from_who=TEXT(stored=True), to_who=TEXT(stored=True), subject=TEXT(stored=True),
                  body=TEXT(stored=True), id=ID(stored=True))


def search_by_recipient(dir_index, query):

    ix = open_dir(dir_index)

    with ix.searcher() as searcher:
        my_query = QueryParser("from_who", ix.schema).parse(query)
        results = searcher.search(my_query, limit=6)
        res = []
        for r in results:
            mail = [r['to_who'], r['subject']]
            res.append(mail)

    return res


def main():
    root = Tk()

    root.title("Mails")
    root.geometry("800x600")

    def initialise():
        create_index("/home/andres/AII/Enunciados/Whoosh/Correos","Index")

    index_button = Button(root, text="Create index", command=initialise)
    index_button.pack(side="top")

    entry = Entry(root)
    entry.pack(side="top")

    def search():
        show_list(search_by_recipient("Index", entry.get()), frame)

    search_button = Button(root, text="Search", command=search)
    search_button.pack(side="top")

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)

    root.mainloop()


def clear_window(tk):
    ls = tk.pack_slaves()
    for l in ls:
        l.destroy()


def show_list(elements, frame):
    clear_window(frame)
    # Scrollbar
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    # Listbox widget
    mylist = Listbox(frame, yscrollcommand=scrollbar.set)
    mylist.pack(fill=BOTH, expand=1)
    scrollbar.config(command=mylist.yview)
    # Add elements to listbox
    if elements is not None:
        for item in elements:
            mylist.insert(END, "Recipient: " + item[0])
            mylist.insert(END, "Subject: " + item[1])
            mylist.insert(END, "")


if __name__ == '__main__':
    main()
