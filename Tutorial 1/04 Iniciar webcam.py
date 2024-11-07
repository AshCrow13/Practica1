import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import imutils
import cv2

#Crear ventana
ventana = tk.Tk()
ventana.geometry("400x370")
ventana.resizable(0,0)
ventana.title("Iniciar Webcam") 

#Funciones de la camara
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

#Boton
BCamara = tk.Button(ventana, text="Iniciar camara", command=camara)
BCamara.place(x=150, y=330, width=90, height=23)

#Cuadro de imagen gris
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240)

ventana.mainloop()

