from tkinter import *
import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable
#////////////////////////////////////////////////////clase analizador//////////////////////////////////////////
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

    def q0(self, caracter: str):
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
            pass
        else:
            self.agregar_error(caracter, self.x, self.y)

    #--------------------------------automata nodos-----------------------------
    def q1(self, caracter: str):
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
                self.agregar_token(self.buffer, self.x, self.y, 'reservada' + self.buffer)
                self.estado = 0
                self.i -= 1

            else:
                self.agregar_token(self.buffer, self.x, self.y, 'identificador')
                self.estado = 0
                self.i -= 1

    def q2(self, caracter: str):
        if caracter == '(")(^")*(")':
            self.estado = 2
            self.buffer += caracter
            self.y += 1
        else:
            self.agregar_token(self.buffer, self.y, self.y, 'cadena')
            self.estado = 0
            self.i -= 1

    def q3(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'virgilla')
        self.estado = 0
        self.i -= 1

    def q4(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'menor que')
        self.estado = 0
        self.i -= 1

    def q5(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'mayor que')
        self.estado = 0
        self.i -= 1

    def q6(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'dos puntos')
        self.estado = 0
        self.i -= 1

    def q7(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'coma')
        self.estado = 0
        self.i -= 1

    def q8(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'abrir corchete')
        self.estado = 0
        self.i -= 1

    def q9(self, caracter: str):
        self.agregar_token(self.buffer, self.x, self.y, 'cerrar corchete')
        self.estado = 0
        self.i -= 1

    # ----------------------------analizador---------------------------
    def analizar(self, cadena):
        cadena = cadena + '$'
        self.listaErrores = []
        self.listaTokens = []
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.q0(cadena[self.i])
            elif self.estado == 1:
                self.q1(cadena[self.i])
            elif self.estado == 2:
                self.q2(cadena[self.i])
            elif self.estado == 3:
                self.q3(cadena[self.i])
            elif self.estado == 4:
                self.q4(cadena[self.i])
            elif self.estado == 5:
                self.q5(cadena[self.i])
            elif self.estado == 6:
                self.q6(cadena[self.i])
            elif self.estado == 7:
                self.q7(cadena[self.i])
            elif self.estado == 8:
                self.q8(cadena[self.i])
            elif self.estado == 9:
                self.q9(cadena[self.i])

            self.i += 1

    #-----------------------------mostrar datos--------------------------
    def mostrartokens(self):
        tabla = PrettyTable()
        tabla.field_names = ["Lexema", "linea", "columna", "tipo"]
        for i in self.listaTokens:
            tabla.add_row([i.lexema, i.x, i.y, i.tipo])
        print(tabla)

    def mostrarerrores(self):
        tabla = PrettyTable()
        tabla.field_names = ["Error", "linea", "columna"]
        for i in self.listaErrores:
            tabla.add_row([i.descripcion, i.x, i.y])
        print(tabla)

#////////////////////////////////////////////////////clase Error//////////////////////////////////////////
class Error:
    def __init__(self, descripcion: str, x: int, y: int):
        self.descripcion = descripcion
        self.x = x
        self.y = y

    def imprimirData(self):
        print(self.descripcion, self.x, self.y)

#////////////////////////////////////////////////////clase Token//////////////////////////////////////////
class Token:
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



