import tkinter as tk 
from tkinter import * 
from PIL import Image 
from PIL import ImageTk 
import imutils 
import cv2 

#ventana 
ventana = tk.Tk() 
ventana.geometry("1070x450") 
ventana.resizable(0,0) 
ventana.title("Recortar foto webcam") 

#Funciones 
def camara(): 
    global capture
    capture = cv2.VideoCapture(0) 
    iniciar() 

def iniciar():
    global capture 
    if capture is not None: 
        ret, frame = capture.read() 
        if ret == True: 
            frame = imutils.resize(frame, width=311) 
            frame = imutils.resize(frame, height=241) 
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            im = Image.fromarray(ImagenCamara) 
            img = ImageTk.PhotoImage(image=im) 
            LImagen.configure(image=img) 
            LImagen.image = img 
            LImagen.after(1, iniciar) 
        else: 
            LImagen.image = "" 
            capture.release() 

#Funcion camara
def Capturar(): 
    global Captura 
    camara = capture 
    return_value, image = camara.read() 
    frame = imutils.resize(image, width=301) 
    frame = imutils.resize(frame, height=221) 
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    im = Image.fromarray(Captura) 
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img) 
    LImagenROI.image = img 

#Funcion detectar mouse
def mostrar_coordenadas(event): 
    coordenadas['text'] = f'x = {event.x} y = {event.y}' 

def recortar():
    global ImgRec 
    Vx1 = int(x1.get()) 
    Vy1 = int(y1.get()) 
    Vx2 = int(x2.get()) 
    Vy2 = int(y2.get()) 
    ImgRec = Captura[Vx1:Vx2, Vy1:Vy2] 
    Im = Image.fromarray(ImgRec) 
    ImRec = ImageTk.PhotoImage(image=Im) 
    LImagenRecorte.configure(image=ImRec) 
    LImagenRecorte.image = ImRec 

#Botones 
BCamara = tk.Button(ventana, text="iniciar camara", command=camara) 
BCamara.place(x=80, y=330, width=90, height=23) 
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar) 
BCapturar.place(x=220, y=330, width=91, height=23)
BRecortar = tk.Button(ventana, text="Recortar", command=recortar) 
BRecortar.place(x=840, y=400, width=80, height=23) 

#Cuadro de imagen 
LImagen = tk.Label(ventana, background="gray") 
LImagen.place(x=50, y=50, width=300, height=240) 
LImagenROI = tk.Label(ventana, background="gray") 
LImagenROI.place(x=390, y=50, width=300, height=240) 
LImagenRecorte = tk.Label(ventana, background="gray") 
LImagenRecorte.place(x=730, y=50, width=300, height=240) 

#Coordenadas
LImagenROI.bind('<Button-1>', mostrar_coordenadas) 

#Label texto 
coordenadasTitulo = tk.Label(ventana, text="Coordenadas") 
coordenadasTitulo.place(x=505, y=310) 
coordenadas = tk.Label(ventana, text="") 
coordenadas.place(x=495, y=330) 
Lx1 = tk.Label(ventana, text="x1") 
Lx1.place(x=790, y=330) 
Ly1 = tk.Label(ventana, text="y1") 
Ly1.place(x=890, y=330) 
Lx2 = tk.Label(ventana, text="x2")
Lx2.place(x=790, y=360) 
Ly2 = tk.Label(ventana, text="y2") 
Ly2.place(x=890, y=360) 

#Spinbox 
x1 = tk.Spinbox(ventana, from_=0, to=298) 
x1.place(x=810, y=330, width=42, height=22) 
y1 = tk.Spinbox(ventana, from_=0, to=239) 
y1.place(x=910, y=330, width=42, height=22) 
x2 = tk.Spinbox(ventana, from_=1, to=298) 
x2.place(x=810, y=360, width=42, height=22) 
y2 = tk.Spinbox(ventana, from_=1, to=239) 
y2.place(x=910, y=360, width=42, height=22) 

ventana.mainloop()
