import tkinter as tk 
from tkinter import * 
from PIL import Image 
from PIL import ImageTk 
import imutils 
import cv2 

#Ventana 
ventana = tk.Tk() 
ventana.geometry("1070x400") 
ventana.resizable(0,0) 
ventana.title("Umbralizacion escala de grises") 

#Funciones camara
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

#Funcion tomar foto 
def Capturar():
    global CapturaG 
    camara = capture 
    return_value, image = camara.read() 
    frame = imutils.resize(image, width=301) 
    frame = imutils.resize(frame, height=221) 
    CapturaG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    imG = Image.fromarray(CapturaG) 
    imgG = ImageTk.PhotoImage(image=imG) 
    LImagenROI.configure(image=imgG) 
    LImagenROI.image = imgG 

#Funcion umbralizacion
def umbralizacion(): 
    global thresh1 
    valor = int(numeroUmbra.get()) 
    ret, thresh1 = cv2.threshold(CapturaG, valor, 255, cv2.THRESH_BINARY) 
    Umbral = Image.fromarray(thresh1) 
    Umbral = ImageTk.PhotoImage(image=Umbral) 
    ImagenUmbra.configure(image=Umbral) 
    ImagenUmbra.image = Umbral 

#Spinbox 
numeroUmbra = tk.Spinbox(ventana, from_=0, to=255) 
numeroUmbra.place(x=800, y=331, width=42, height=23) 

#Botones 
BCamara = tk.Button(ventana, text="Iniciar camara", command=camara) 
BCamara.place(x=150, y=330, width=90, height=23) 
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar) 
BCapturar.place(x=500, y=330, width=91, height=23) 
Umbra = tk.Button(ventana, text="Umbralizacion", command=umbralizacion) 
Umbra.place(x=860, y=330, width=80, height=23) 

#cuadro de imagen gris 
LImagen = tk.Label(ventana, background="gray") 
LImagen.place(x=50, y=50, width=300, height=240) 
LImagenROI = tk.Label(ventana, background="gray") 
LImagenROI.place(x=390, y=50, width=300, height=240) 
ImagenUmbra = tk.Label(ventana, background="gray") 
ImagenUmbra.place(x=730, y=50, width=300, height=240) 

ventana.mainloop()


