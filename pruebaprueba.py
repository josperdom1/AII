from tkinter import *


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
        mylist.insert(END, "Precio normal: " + item[3])
        if item[4] != null:
            mylist.insert(END, "Precio de oferta: " + item[4])
        mylist.insert(END, "")


if __name__ == '__main__':
    print("Hola mundo")
    root = Tk()
    root.geometry("300x150")


    def clear_window(tk):
        ls = tk.pack_slaves()
        for l in ls:
            l.destroy()


    def store_products():
        print("Store products")


    def show_brand():
        print("Hola mundo")
        new_window = Toplevel()
        # new_window.geometry("800x600")
        # frame = Frame(new_window)
        # frame.pack()
        # brands = get_brands()
        # spinbox = Spinbox(frame, values=brands)
        # spinbox.pack(side="left")
        # results_frame = Frame(new_window)
        # results_frame.pack(fill=BOTH, expand=1)
        #
        # def search_brand_caller():
        #    clear_window(results_frame)
        #    search_brand(entry.get(), results_frame)
        #
        # b = Button(frame, text="Buscar", command=search_brand_caller)
        # b.pack(side="right")
        # new_window.mainloop()


    store_products_btn = Button(root, text="Almacenar productos", command=store_products)
    store_products_btn.pack()

    show_brand_btn = Button(root, text="Mostrar marca", command="show_brand")
    show_brand_btn.pack()

    search_deals_btn = Button(root, text="Buscar ofertas", command="search_deals")
    search_deals_btn.pack()

    root.mainloop()
