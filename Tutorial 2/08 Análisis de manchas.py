import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageTk
from PIL import ImageGrab
import numpy as np
import imutils
import cv2
from datetime import datetime

#ventana
ventana = tk.Tk()
ventana.geometry("1150x500")
ventana.title("Analisis de Manchas")
global img, imageToShow, Captura, valor, Region

def archivo():
    try:
        #Lee la imagen
        path_image = filedialog.askopenfilename(filetype=[
            ("image", "jpg"),
            ("image", "jpeg"),
            ("image", "png")])
        if len(path_image) > 0:
            global imagenFile, img, imageToShow, valor
            imagenFile = cv2.imread(path_image)
            imagenFile = imutils.resize(imagenFile, height=240)
            imagenFile = imutils.resize(imagenFile, width=300)
            imageToShow = cv2.cvtColor(imagenFile, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            LImagenROI.configure(image=img)
            LImagenROI.image = img
            LImagenManchas.configure(image= img)
            LImagenManchas.image = img
            valor = 0
            ROI()
    except :
        messagebox.showerror(message="El archivo seleccionado no es un tipo de imagen válido")

def camara():
    global capture
    capture = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
    iniciar()
    
def iniciar():
    global capture
    if capture is not None:
        BCapturar.place(x=150, y=420, width=91, height=23)
        ret, frame = capture.read()
        if ret == True:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img = ImageTk.PhotoImage(image=im)
            LImagen.configure(image=img)
            LImagen.image = img
            LImagen.after(10, iniciar)
        else:
            LImagen.image = ""
            capture.release()

def Capturar():
    global valor, Captura
    camara = capture
    return_value, image = camara.read()
    frame = imutils.resize(image, width=301)
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagenROI.configure(image=img)
    LImagenROI.image = img
    valor = 1

def ROI(*args):
    global Region, imagen_recortada
    x1 = int(SImagen1A.get())
    x2 = int(SImagen1B.get())
    y1 = int(SImagen1I.get())
    y2 = int(SImagen1D.get())
    # Obtiene las dimensiones de la imagen
    alto, ancho = imageToShow.shape[:2]
    # Crea una máscara con los límites especificados
    mascara = np.zeros((alto, ancho), np.uint8)
    mascara[y2:y1, x1:x2] = 255
    # Aplica la máscara a la imagen
    imagen_recortada = cv2.bitwise_and(imageToShow, imageToShow, mask=mascara)
    # Devuelve la imagen recortada
    aux = Image.fromarray(imagen_recortada)
    Region = ImageTk.PhotoImage(image=aux)
    LImagenROI.configure(image=Region)
    LImagenROI.image = Region

def rgb():
    Minimos = (int(SRedI.get()),int(SGreenI.get()),int(SBlueI.get()))
    Maximos = (int(SRedD.get()),int(SGreenD.get()),int(SBlueD.get()))
    if valor == 0:
        #modificar este con el resultado de la ROI
        img_mask = cv2.inRange(imageToShow, Minimos, Maximos)
    if valor == 1:
        img_mask = cv2.inRange(Captura, Minimos, Maximos)
    img_aux = img_mask
    img_mask = Image.fromarray(img_mask)
    img_mask = ImageTk.PhotoImage(image=img_mask)
    LImagenManchas.configure(image=img_mask)
    LImagenManchas.image = img_mask
    _, bin_imagen = cv2.threshold(img_aux, 0, 255, cv2.THRESH_BINARY_INV)
    # Contar el número de píxeles con manchas
    num_pixels_con_manchas = cv2.countNonZero(bin_imagen)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = 100 - (num_pixels_con_manchas/bin_imagen.size) * 100
    #Contornos
    contornos = cv2.findContours(img_aux, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    area = 0
    #Area de contornos
    area = (bin_imagen.size/(num_pixels_con_manchas/bin_imagen.size))
    #Cantida de contornos
    num_formas = len(contornos)
    Cadena = f"Cantidad de manchas detectada:{num_formas}\nArea Mancha: {area}\nPorcentaje de manchas:{round(porcentaje_manchas, 2)}%"
    CajaTexto.configure(state='normal')
    CajaTexto.delete(1.0, tk.END)
    CajaTexto.insert(1.0, Cadena)
    CajaTexto.configure(state='disabled')

def guardar():
    x1 = int(SImagen1A.get())
    x2 = int(SImagen1B.get())
    y1 = int(SImagen1I.get())
    y2 = int(SImagen1D.get())
    global imagen_recortada    
    imagen_recortada = imagen_recortada[y2:y1, x1:x2, :]
    cv2.imwrite("Recortada.jpg", imagen_recortada)
    imagen_recortada = Image.fromarray(imagen_recortada)
    imagen_recortada = ImageTk.PhotoImage(image=imagen_recortada)
    LImagenManchas.configure(image=imagen_recortada)
    LImagenManchas.image = imagen_recortada

#Botones
BArchivo = tk.Button(ventana, text="Archivo", command=archivo)
BArchivo.place(x=60, y=370,width=75,height=23)
BCamara = tk.Button(ventana, text="Camara", command=camara)
BCamara.place(x=260, y=370, width=75, height=23)
BCapturar = tk.Button(ventana, text="Iniciar captura", command=Capturar)
BGuardar = tk.Button(ventana, text="Guardar", command=guardar)
BGuardar.place(x=540, y=300, width=75, height=23)
BManchas = tk.Button(ventana, text="Analisis de Manchas", command=rgb)
BManchas.place(x=890, y=250, width=131, height=23)

#Label
LCargar = tk.Label(ventana, text="Cargar Imagen")
LCargar.place(x=160, y=370, width=81, height=16)
LRed = tk.Label(ventana, text="R")
LRed.place(x=570, y=360, width=21, height=16)
LGreen = tk.Label(ventana, text="G")
LGreen.place(x=570, y=400, width=21, height=16)
LBlue = tk.Label(ventana, text="B")
LBlue.place(x=570, y=440, width=21, height=16)

#Cuadros de Imagen
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50, y=50, width=300, height=240)
LImagenROI = tk.Label(ventana, background="gray")
LImagenROI.place(x=430, y=50, width=300, height=240)
LImagenManchas = tk.Label(ventana, background="gray")
LImagenManchas.place(x=810, y=20, width=301, height=221)

#Cuadro de Texto
CajaTexto = tk.Text(ventana, state="disabled")
CajaTexto.place(x=820, y=300, width=311, height=121)

#Sliders
SImagen1A = tk.Scale(ventana, from_=0, to=300, orient='horizontal', command=ROI)
SImagen1A.place(x=50,y=5, width=311)
SImagen1I = tk.Scale(ventana, from_=0, to=240, orient='vertical', command=ROI)
SImagen1I.set(240)
SImagen1I.place(x=5,y=50, height=241)
SImagen1B = tk.Scale(ventana, from_=0, to=300, orient='horizontal', command=ROI)
SImagen1B.set(300)
SImagen1B.place(x=50,y=295, width=311)
SImagen1D = tk.Scale(ventana, from_=0, to=240, orient='vertical', command=ROI)
SImagen1D.place(x=360, y=50, height=241)

SRedI = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SRedI.place(x=430,y=340)
SGreenI = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SGreenI.place(x=430, y= 380)
SBlueI = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SBlueI.place(x=430, y= 420)

SRedD = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SRedD.set(255)
SRedD.place(x=630,y=340)
SGreenD = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SGreenD.set(255)
SGreenD.place(x=630, y= 380)
SBlueD = tk.Scale(ventana, from_=0, to=255, orient='horizontal')
SBlueD.set(255)
SBlueD.place(x=630, y= 420)

ventana.mainloop()
