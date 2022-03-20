from tkinter import *
import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable

class analizador:
    def __init__(self) -> None:
        self.tokens = []
        self.errores = []
        self.x = 1
        self.y = 0
        self.buffer = ''
        self.estado = 0
        self.i = 0

    def agregar_token(self, caracter, x, y, token):
        self.listaTokens.append(Token(caracter, x, y, token))
        self.buffer = ''

    def agregar_error(self, caracter, x, y):
        self.listaErrores.append(Error('Caracter ' + caracter + ' no reconocido en el lenguaje.', x, y))

    def s0(self, caracter: str):
        '''Estado S0'''
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.y += 1
        elif caracter == '(")(^")*(")':
            self.estado = 2
            self.buffer += caracter
            self.y += 1
        elif caracter == '~':
            self.estado = 3
            self.buffer += caracter
            self.y += 1
        elif caracter == '<':
            self.estado = 4
            self.buffer += caracter
            self.y += 1
        elif caracter == '>':
            self.estado = 5
            self.buffer += caracter
            self.y += 1
        elif caracter == ':':
            self.estado = 6
            self.buffer += caracter
            self.y += 1
        elif caracter == ',':
            self.estado = 7
            self.buffer += caracter
            self.y += 1
        elif caracter == '[':
            self.estado = 8
            self.buffer += caracter
            self.y += 1
        elif caracter == ']':
            self.estado = 9
            self.buffer += caracter
            self.y += 1
        elif caracter == '\n':
            self.x += 1
            self.y = 0
        elif caracter in ['\t', ' ']:
            self.y += 1
        elif caracter == '$':
            print('Se terminó el análisis')
        else:
            self.agregar_error(caracter, self.x, self.y)

    def s1(self, caracter: str):
        '''Estado S1'''
        if caracter.isalpha():
            self.estado = 1
            self.buffer += caracter
            self.y += 1
        elif caracter.isdigit():
            self.estado = 1
            self.buffer += caracter
            self.y += 1
        else:
            if self.buffer in ['tipo', 'valor', 'fondo', 'valores', 'nombre']:
                self.agregar_token(self.buffer, self.x, self.y, 'reservada_' + self.buffer)
                self.estado = 0
                self.i -= 1

            else:
                self.agregar_token(self.buffer, self.x, self.y, 'identificador')
                self.estado = 0
                self.i -= 1

    def s2(self, caracter: str):
        '''Estado S2'''
        if caracter == '(")(^")*(")':
            self.estado = 2
            self.buffer += caracter
            self.y += 1
        else:
            self.agregar_token(self.buffer, self.y, self.y, 'cadena')
            self.estado = 0
            self.i -= 1

    def s3(self, caracter: str):
        '''Estado S3'''
        self.agregar_token(self.buffer, self.x, self.y, 'parentesisIzquierdo')
        self.estado = 0
        self.i -= 1

    def s4(self, caracter: str):
        '''Estado S4'''
        self.agregar_token(self.buffer, self.x, self.y, 'parentesisDerecho')
        self.estado = 0
        self.i -= 1

    def s5(self, caracter: str):
        '''Estado S5'''
        self.agregar_token(self.buffer, self.x, self.y, 'puntoYComa')
        self.estado = 0
        self.i -= 1

    def s6(self, caracter: str):
        '''Estado S6'''
        self.agregar_token(self.buffer, self.x, self.y, 'signoIgual')
        self.estado = 0
        self.i -= 1

    def s7(self, caracter: str):
        '''Estado S7'''
        self.agregar_token(self.buffer, self.x, self.y, 'coma')
        self.estado = 0
        self.i -= 1

    def s8(self, caracter: str):
        '''Estado S7'''
        self.agregar_token(self.buffer, self.x, self.y, 'coma')
        self.estado = 0
        self.i -= 1

    def s9(self, caracter: str):
        '''Estado S7'''
        self.agregar_token(self.buffer, self.x, self.y, 'coma')
        self.estado = 0
        self.i -= 1

    def analizar(self, cadena):
        cadena = cadena + '$'
        self.listaErrores = []
        self.listaTokens = []
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.s0(cadena[self.i])
            elif self.estado == 1:
                self.s1(cadena[self.i])
            elif self.estado == 2:
                self.s2(cadena[self.i])
            elif self.estado == 3:
                self.s3(cadena[self.i])
            elif self.estado == 4:
                self.s4(cadena[self.i])
            elif self.estado == 5:
                self.s5(cadena[self.i])
            elif self.estado == 6:
                self.s6(cadena[self.i])
            elif self.estado == 7:
                self.s7(cadena[self.i])
            elif self.estado == 8:
                self.s8(cadena[self.i])
            elif self.estado == 9:
                self.s9(cadena[self.i])

            self.i += 1

    def mostrartokens(self):
        '''Imprime una tabla con los tokens'''
        tabla = PrettyTable()
        tabla.field_names = ["Lexema", "linea", "columna", "tipo"]
        for i in self.listaTokens:
            tabla.add_row([i.lexema, i.x, i.y, i.tipo])
        print(tabla)

    def mostrarerrores(self):
        '''Imprime una tabla con los errores'''
        tabla = PrettyTable()
        tabla.field_names = ["Error", "linea", "columna"]
        for i in self.listaErrores:
            tabla.add_row([i.descripcion, i.x, i.y])
        print(tabla)


class Error:

    def __init__(self, descripcion: str, x: int, y: int):
        self.descripcion = descripcion
        self.x = x
        self.y = y

    def imprimirData(self):
        print(self.descripcion, self.x, self.y)


class Token:
    '''Clase TOken'''
    def __init__(self,lexema : str,x : int,y : int,tipo : str) -> None:
        self.lexema = lexema
        self.x = x
        self.y = y
        self.tipo = tipo

    def imprimirData(self):
        print(self.lexema, self.x, self.y, self.tipo)

lexico = analizador()
def leer():
    archivo = filedialog.askopenfilename(initialdir="/",
                                         title="Select a File",
                                         filetypes=(("Text files", "*.form*"), ("all files", "*.*")))

    if archivo != '':
        archi1 = open(archivo, "r", encoding="utf-8")
        contenido = archi1.read()
        archi1.close()
        area.delete("1.0", tk.END)
        area.insert("1.0", contenido)

        lexico.analizar(contenido)
        lexico.mostrartokens()
        lexico.mostrarerrores()


ventana = Tk()
ventana.title("Proyecto 1 LFP")
frame = Frame(ventana, width=600, height=450)
frame.pack()
reportes = Label(frame, text="Reportes: ")
reportes.place(x=350, y=10)
area = Text(frame, width=72, height=20)
area.place(x=10, y=50)
scroll = Scrollbar(frame, command=area.yview())
area.config(yscrollcommand=scroll.set)
menu = Button(frame, text="Archivo", command=leer)
menu.place(x=240, y=400)
analizar = Button(frame, text="Analizar")
analizar.place(x=310, y=400)
ventana.mainloop()



