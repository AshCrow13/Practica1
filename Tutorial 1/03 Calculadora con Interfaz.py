from tkinter import *
import numpy as np 

#Codigo Ventana
ventana = Tk() 
ventana.title("Calculadora")
ventana.geometry("400x190") 
ventana.resizable(0,0) 

#ventana.mainloop() 

#textos
textoUno = Label(ventana, text="Valor1") 
textoDos = Label(ventana, text="Valor2") 
textoUno.grid(row=0, column=0, padx=5, pady=5) 
textoDos.grid(row=0, column=3, padx=5, pady=5) 

#entradas
entradaUno = Entry(ventana) 
entradaDos = Entry(ventana) 
entradaSuma = Entry(ventana, state="readonly") 
entradaResta = Entry(ventana, state=DISABLED) 
entradaMultiplicacion = Entry(ventana, state=DISABLED) 
entradaDivision = Entry(ventana, state=DISABLED) 
entradaUno.grid(row=0, column=1, padx=5, pady=5) 
entradaDos.grid(row=0, column=4, padx=5, pady=5) 
entradaSuma.grid(row=1, column=1, padx=5, pady=5) 
entradaResta.grid(row=2, column=1, padx=5, pady=5) 
entradaMultiplicacion.grid(row=3, column=1, padx=5, pady=5) 
entradaDivision.grid(row=4, column=1, padx=5, pady=5) 

#botones
botonSuma = Button(ventana, text="Suma", width=8, height=1, command=lambda:clickBotonSuma(entradaUno.get(), entradaDos.get())) 
botonResta = Button(ventana, text="Resta", width=8, height=1, command=lambda:clickBotonResta(entradaUno.get(), entradaDos.get())) 
botonMultiplicacion = Button(ventana, text="Multiplicar", width=8, height=1, command=lambda:clickBotonMultiplicacion(entradaUno.get(), entradaDos.get())) 
botonDivision = Button(ventana, text="Dividir", width=8, height=1, command=lambda:clickBotonDivision(entradaUno.get(), entradaDos.get()))
botonSuma.grid(row=1, column=0, padx=5, pady=5)
botonResta.grid(row=2, column=0, padx=5, pady=5)
botonMultiplicacion.grid(row=3, column=0, padx=5, pady=5)
botonDivision.grid(row=4, column=0, padx=5, pady=5) 

#funciones de la calculadora
def clickBotonSuma(x,y):
    entradaSuma.configure(state=NORMAL) 
    entradaSuma.delete(0, END) 
    entradaSuma.insert(0, f"{int(x)+int(y)}")
    entradaSuma.configure(state=DISABLED) 
    botonSuma.configure(background="DARKGRAY") 

def clickBotonResta(x,y):
    entradaResta.configure(state=NORMAL) 
    entradaResta.delete(0, END) 
    entradaResta.insert(0, f"{int(x)-int(y)}") 
    entradaResta.configure(state=DISABLED) 
    botonResta.configure(background="DARKGRAY") 

def clickBotonMultiplicacion(x,y):
    entradaMultiplicacion.configure(state=NORMAL) 
    entradaMultiplicacion.delete(0, END) 
    entradaMultiplicacion.insert(0, f"{int(x)*int(y)}")
    entradaMultiplicacion.configure(state=DISABLED) 
    botonMultiplicacion.configure(background="DARKGRAY")

def clickBotonDivision(x,y):
    entradaDivision.configure(state=NORMAL) 
    entradaDivision.delete(0, END) 
    entradaDivision.insert(0, f"{np.double(x)/np.double(y)}") 
    entradaDivision.configure(state=DISABLED) 
    botonDivision.configure(background="DARKGRAY") 

ventana.mainloop() 


