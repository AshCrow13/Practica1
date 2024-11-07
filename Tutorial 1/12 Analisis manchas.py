import tkinter as tk 
from tkinter import *
from PIL import Image 
from PIL import ImageTk 
import imutils 
import cv2 

#Crear ventana 
ventana = tk.Tk() 
ventana.geometry("1320x470") 
ventana.resizable(0,0) 
ventana.title("Analizador de manchas") 

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

#Funcion para tomar foto 
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

def rgb(): 
    global img_mask, img_aux, bin_imagen
    Minimos = (int(SRedI.get()), int(SGreenI.get()), int(SBlueI.get()))
    Maximos = (int(SRedD.get()), int(SGreenD.get()), int(SBlueD.get())) 
    img_mask = cv2.inRange(Captura, Minimos, Maximos) 
    img_aux = img_mask
    img_mask = Image.fromarray(img_mask) 
    img_mask = ImageTk.PhotoImage(image=img_mask) 
    ImagenUmbra.configure(image=img_mask) 
    ImagenUmbra.image = img_mask 
    _, bin_imagen = cv2.threshold(img_aux, 0, 255, cv2.THRESH_BINARY_INV) 

def manchas(): 
    #Contar el numero e pixeles con manchas 
    num_pixels_con_manchas = cv2.countNonZero(bin_imagen) 
    #Calcular el porcentaje de manchas 
    porcentaje_manchas = 100 - (num_pixels_con_manchas/bin_imagen.size) * 100 
    #Contornos 
    contornos = cv2.findContours(img_aux, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0] 
    #Cantidad de contornos 
    num_formas = len(contornos) 
    Cadena = f"Cantidad de manchas blancas: {num_formas}\nPorcentaje area con manchas: {round(porcentaje_manchas, 2)}%" 
    CajaTexto.configure(state='normal') 
    CajaTexto.delete(1.0, tk.END) 
    CajaTexto.insert(1.0, Cadena) 
    CajaTexto.configure(state='disabled') 

#RGB se inicia en 1 
SRedI = tk.Scale(ventana,from_=1, to=255, orient='horizontal') 
SRedI.place(x=760, y=300) 
SGreenI = tk.Scale(ventana, from_=1, to=255, orient='horizontal') 
SGreenI.place(x=760, y=340) 
SBlueI = tk.Scale(ventana, from_=1, to=255, orient='horizontal')
SBlueI.place(x=760, y=380) 

SRedD = tk.Scale(ventana, from_=1, to=255, orient='horizontal') 
SRedD.set(255) 
SRedD.place(x=900, y=300) 
SGreenD = tk.Scale(ventana, from_=1, to=255, orient='horizontal') 
SGreenD.set(255) 
SGreenD.place(x=900, y=340) 
SBlueD = tk.Scale(ventana, from_=1, to=255, orient='horizontal') 
SBlueD.set(255) 
SBlueD.place(x=900, y=380) 

#Label 
LRed = tk.Label(ventana, text="R") 
LRed.place(x=870, y=320, width=21, height=16) 
LGreen = tk.Label(ventana, text="G") 
LGreen.place(x=870, y=360, width=21, height=16) 
LBlue = tk.Label(ventana, text="B") 
LBlue.place(x=870, y=400, width=21, height=16) 

#Botones 
BCamara = tk.Button(ventana, text="Iniciar camara", command=camara) 
BCamara.place(x=150, y=330, width=90, height=23) 
BCapturar = tk.Button(ventana, text="Tomar foto", command=Capturar) 
BCapturar.place(x=500, y=330, width=91, height=23) 
Umbra = tk.Button(ventana, text="Umbralizacion", command=rgb) 
Umbra.place(x=840, y=430, width=80, height=23) 
Manchas = tk.Button(ventana, text="Analisis de manchas", command=manchas) 
Manchas.place(x=1120, y=330, width=120, height=23) 

#Cuadros de imagen gris
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240) 
LImagenROI = tk.Label(ventana, background="gray") 
LImagenROI.place(x=390, y=50, width=300, height=240) 
ImagenUmbra = tk.Label(ventana, background="gray") 
ImagenUmbra.place(x=730, y=50, width=300, height=240) 

#Cuadro de texto 
CajaTexto = tk.Text(ventana, state="disabled") 
CajaTexto.place(x=1055, y=50, width=225, height=220) 

ventana.mainloop()

