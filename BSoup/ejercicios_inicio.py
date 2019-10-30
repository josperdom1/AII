import string
from string import digits

def containsnumbers(value):
    return any(char in digits for char in value)

def separadorComas(palabra):
    nuevaPalabra = ""
    for letra in palabra:
        nuevaPalabra =  nuevaPalabra + letra + ","
    print(nuevaPalabra[:-1])

separadorComas("separar")


def sustituyeBlank(texto):
    texto2 = texto.replace(" ","_",-1)
    print(texto2)

sustituyeBlank("Esto es un texto con espacios")

def reemplazaNumeros(str):
    for c in str:
        if c.isdigit():
           str = str.replace(c,"X")
    print(str)

reemplazaNumeros("Tu contraseña es : 12334123")

def insert_dot(string, index):
    return string[:index] + '.' + string[index:]

def addDot(ip):
    i=0
    while i < len(ip):
        i = i+3
        insert_dot(ip,i)
    print(ip)


addDot("2555255552555255")
