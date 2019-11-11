import os

from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from datetime import datetime


def get_email_schema():
    return Schema(id=ID(stored=True), sender=TEXT(stored=True, phrase=False),
                  recipients=TEXT(stored=True), date=DATETIME(stored=True),
                  subject=TEXT(stored=True), body=TEXT)


def get_contacts_schema():
    return Schema(email=ID(stored=True), name=TEXT(stored=True))


def create_email_index(dir_index, dir_emails):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_email_schema())
    writer = ind.writer()

    for doc_name in os.listdir(dir_emails):
        if not os.path.isdir(dir_emails + doc_name):
            add_doc(writer, dir_emails, doc_name)

    writer.commit()
    print("Email index created successfully")


def create_contacts_index(dir_index, dir_contacts):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)

    ind = create_in(dir_index, schema=get_contacts_schema())
    writer = ind.writer()

    file = open(dir_contacts)
    lines = file.readlines()

    for line1, line2 in zip(lines[0::2], lines[1::2]):
        email = line1.strip()
        name = line2.strip()
        writer.add_document(email=email, name=name)

    writer.commit()
    print("Contact index created successfully")


def add_doc(writer, path, doc_name):
    file = open(path + "/" + doc_name)
    sender = file.readline().strip()
    recipients = file.readline().strip()
    date_str = file.readline().strip()
    date = datetime.strptime(date_str, "%Y%m%d")
    subject = file.readline().strip()

    readlines = file.readlines()
    body = " ".join(readlines)

    writer.add_document(id=doc_name, sender=sender, recipients=recipients,
                        date=date, subject=subject, body=body)


def search_name_by_email_address(email):
    ix = open_dir("contacts_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("email", ix.schema).parse(email)
        results = searcher.search(my_query, limit=1)
        try:
            return results[0]["name"]
        except:
            return email


def search_emails(text):
    ix = open_dir("email_index")

    with ix.searcher() as searcher:
        my_query = MultifieldParser(["subject", "body"], ix.schema).parse(text)
        results = searcher.search(my_query, limit=None)
        emails = [[search_name_by_email_address(r["sender"]), r["subject"]] for r in results]

    return emails


def search_emails_after_date(date):
    ix = open_dir("email_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("date", ix.schema).parse("date:[" + date + " to]")
        results = searcher.search(my_query, limit=None)
        emails = [[r["sender"], r["recipients"], r["subject"]] for r in results]

    return emails


def get_files_with_spam(spamwords):
    ix = open_dir("email_index")

    with ix.searcher() as searcher:
        my_query = QueryParser("subject", ix.schema).parse(spamwords.replace(" ", " OR "))
        results = searcher.search(my_query, limit=None)
        filenames = [r["id"] for r in results]

    return filenames

def main():
    create_email_index("email_index", "/home/andres/AII/Enunciados/Whoosh/Ejercicio 2/Correos")
    create_contacts_index("contacts_index", "/home/andres/AII/Enunciados/Whoosh/Ejercicio 2/Agenda/agenda.txt")
    print(search_emails("noticias"))

    print("Select an option: \n"
          "1) Search sender and subject by body or subject \n"
          "2) Search sender recipient and subject after the given date in format YYYYMMDD\n"
          "3) Search files name by spam words in the subject Ex: Contrato Gracias compraventa \n")

    switch(input){
        case 1:

        break;
        case 2:

        break;
        case 3:

        break;
        default:
        print("select an option beetween 1 and 3")
    }


if __name__ == '__main__':
    main()