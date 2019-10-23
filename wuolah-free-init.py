# -*- coding: utf-8 -*-

import sqlite3
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request



def extraerDatosURL():
    pagina = urllib.request.urlopen("http://www.us.es/rss/feed/portada").read()
    soup = BeautifulSoup(pagina, 'html.parser')

    divsJornadas = soup.find_all('div', class_ = ["cont-resultados cf"]) 
    #Con esto podemos acceder a los divs que tengan la class concreta y crear una lista con cada div coincidente y todo lo que contiene el div

    resultados=[]

    for div in divsJornadas:
        tablaJornada=div.find("tbody") #encuentra una ocurrencia con la etiqueta estipulada
        jornada=tablaJornada.find_all('tr')
        
        for partido in jornada:
            jornadaN = divsJornadas.index(div)+1
            local=partido.find('td', class_ = ["col-equipo-local"]).a.span.text
            visitante=partido.find('td', class_ = ["col-equipo-visitante"]).a
            visitante = visitante.find('span', class_ = ["nombre-equipo"]).text
            resultado = partido.find('td', class_ = ["col-resultado finalizado"]).a.text.strip().split() #strip elimina los caracteres como parámetro de la cadena, por defecto los espacios en blanco
            link= partido.find('a',class_ =["resultado"])
            
            tuplaEquiposResultado = (jornadaN, local,visitante,str(resultado[0]+resultado[1]+resultado[2]),str("https://resultados.as.com"+link["href"]))
            resultados.append(tuplaEquiposResultado)
            
    print(resultados)
    return resultados


def crearBBDD():
   
    datos=extraerDatosURL()
    
    baseDatos = sqlite3.connect('partidosLiga.db')  # se conecta a la base de datos del parámentro o, si no existe, la crea
    cursor = baseDatos.cursor()
    
    cursor.execute("""drop table if exists liga""")
    cursor.execute("""create table liga (jornada int not null, local text not null, visitante text not null, resultado text not null, link text)""")
      
    for partido in datos: 
        jornadaN = partido[0]
        local = partido[1]
        visitante = partido[2]
        resultado = partido[3]
        link = partido[4]
        cursor.execute("""insert into liga(jornada,local,visitante,resultado, link) values(?,?,?,?,?)""",(jornadaN, local, visitante, resultado, link))
    
    baseDatos.commit() #importante guardar el resultado de las operaciones realizadas en la base de datos
    
    cursor = baseDatos.execute("SELECT COUNT(*) FROM LIGA") #Número de filas guardadas en la bbdd
    messagebox.showinfo("Terminado","Base de datos creada correctamente. Se han guardado " + str(cursor.fetchone()[0]) + " elementos")
    #fetchone recupera la informaicón de la consulta guardada en el cursor
    #cuando los datos son una colección fetchone recupera el primer elemento y en cada ejecución el siguiente
    baseDatos.close()

def listarDatos():
    baseDatos = sqlite3.connect('partidosLiga.db')
    cursor = baseDatos.cursor()
    
    cursor.execute("""SELECT COUNT (*) FROM LIGA""")
    numeroElementos = cursor.fetchone()[0]
    
    cursor.execute("""SELECT distinct jornada FROM LIGA""")
    jornadas=cursor.fetchall()
    
    lista = Toplevel()
    scrollbar = Scrollbar(lista)
    scrollbar.pack( side = RIGHT, fill = Y)
    lista.title("Resultados de la Liga 17/18")
    texto = Text(lista,width=150, yscrollcommand=scrollbar.set)
    texto.insert(INSERT, "Encontrados {0} resultados: \n".format(numeroElementos))
    
    for i in range (1,len(jornadas)+1):
        texto.insert(INSERT, "Jornada "+str(i)+"\n")
        texto.insert(INSERT, "\n")
        cursor.execute("""SELECT local,visitante,resultado,link FROM LIGA WHERE jornada = ?""",(i,))
        partidos=cursor.fetchall() 
        for partido in partidos:
            texto.insert(INSERT, partido[0]+" "+partido[2]+" "+partido[1]+"  Crónica: "+partido[3]+"\n")
        texto.insert(INSERT, "\n")
        
    
    texto.pack(side = LEFT, fill = BOTH)
    scrollbar.config(command = texto.yview)    
    
if __name__ == "__main__":
    
    ventana = Tk()
    ventana.title('Noticias')
    almacenar = Button(ventana, text="Almacenar", command=crearBBDD)
    almacenar.pack(side=LEFT)
    listar = Button(ventana,text ="Listar", command=listarDatos)
    listar.pack(side=LEFT)
    ventana.mainloop()

    

