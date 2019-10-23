import sqlite3
from tkinter import *
from tkinter import messagebox
import urllib.request
from bs4 import BeautifulSoup


def extract():
    html_doc = urllib.request.urlopen("https://www.ulabox.com/campaign/productos-sin-gluten#gref").read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    articles = soup.find_all('article')

    products = []

    for a in articles:
        product = []

        hgroup = a.find('hgroup')
        product_brand = hgroup.find('h4').find('a').string
        product_name = hgroup.find('h3').find('a').string
        product_link = hgroup.find('h3').find('a').get('href')
        product_price = a.find('span', class_='delta').string + a.find('span', class_='milli').string[0:3]
        product_sale = a.find('del',
                              class_='product-item__price product-item__price--old product-grid-footer__price--old nano | flush--bottom')

        product.append(product_brand.strip())
        product.append(product_name.strip())
        product.append(product_link)
        product.append(float(product_price.replace(',', '.')))

        if product_sale is not None:
            product.append(float(product_sale.string[0:4].replace(',', '.')))

        products.append(product)

    return products


def create_db():
    products = extract()

    db = sqlite3.connect('products.db')  # conectando a la base de datos
    cursor = db.cursor()

    cursor.execute("""DROP TABLE if exists producto""")  # si existe la tabla 'producto' la elimina
    # creamos la tabla producto: marca, nombre, link a la descripcion del producto y precio/s (si est en oferta tiene de un precio).
    cursor.execute(
        """CREATE TABLE producto (marca text not null, nombre text not null, link text not null, precio real not null, oferta real)""")

    for product in products:
        marca = product[0]
        nombre = product[1]
        link = product[2]
        precio = product[3]
        oferta = None
        if len(product) == 5:
            oferta = product[4]

        cursor.execute("""INSERT INTO producto (marca, nombre, link , precio, oferta) values(?,?,?,?,?)"""
                       , (marca, nombre, link, precio, oferta))

    db.commit()  # guardar el resultado de las operaciones realizadas en la BDD

    cursor = db.execute("SELECT COUNT(*) FROM PRODUCTO")  # numero de filas guardadas
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
        mylist.insert(END, "Marca: " + item[0])
        mylist.insert(END, "Nombre: " + item[1])
        mylist.insert(END, "Link: " + item[2])
        mylist.insert(END, "Precio normal: " + str(item[3]))
        if item[4] != None:
            mylist.insert(END, "Precio de oferta: " + str(item[4]))
        mylist.insert(END, "")


def search_brand(query, tk):
    db = sqlite3.connect('products.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM PRODUCTO WHERE MARCA = '" + query + "'")
    show_list(cursor.fetchall(), tk)


def clear_window(tk):
    ls = tk.pack_slaves()
    for l in ls:
        l.destroy()


def show_main_buttons():
    store_products_btn = Button(root, text="Almacenar productos", command=create_db)
    store_products_btn.pack()

    show_brand_btn = Button(root, text="Mostrar marca", command=show_brand)
    show_brand_btn.pack()

    search_deals_btn = Button(root, text="Buscar ofertas", command=search_deals)
    search_deals_btn.pack()


def get_brands():
    db = sqlite3.connect('products.db')
    db.text_factory = str
    cursor = db.cursor()

    brands_list = cursor.execute("SELECT MARCA FROM PRODUCTO")

    ls = []
    for m in brands_list:
        ls.append(m[0])

    return ls


def show_brand():
    new_window = Toplevel()
    new_window.title("Buscar por marca")
    new_window.geometry("800x600")
    frame = Frame(new_window)
    frame.pack()
    brands = get_brands()
    spinbox = Spinbox(frame, values=brands)
    spinbox.pack(side="left")
    results_frame = Frame(new_window)
    results_frame.pack(fill=BOTH, expand=1)

    def search_brand_caller():
        clear_window(results_frame)
        search_brand(spinbox.get(), results_frame)

    b = Button(frame, text="Buscar", command=search_brand_caller)
    b.pack(side="right")


def search_deals():  # TODO
    new_window = Toplevel()
    new_window.title("Ofertas")
    new_window.geometry("800x600")

    db = sqlite3.connect('products.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM PRODUCTO WHERE OFERTA NOT NULL")

    prods_oferta = cursor.fetchall()

    show_list(prods_oferta, new_window)


if __name__ == '__main__':
    root = Tk()
    root.title("Ulabox Scrapper")
    root.geometry("300x150")

    show_main_buttons()

    root.mainloop()