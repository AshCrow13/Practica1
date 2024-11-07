import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageTk
import imutils
import cv2

#Ventana
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("Grises")

#Imagen
imagenFile = None
def elegir_imagen():
    try:
        path_image = filedialog.askopenfilename(filetype=[
            ("image", "jpg"),
            ("image", "jpeg"),
            ("image", "png")])
        if len(path_image) > 0:
            global imagenFile, imagenFile2
            #Lee la imagen
            imagenFile = cv2.imread(path_image)
            imagenFile2 = cv2.imread(path_image)
            imagenFile = imutils.resize(imagenFile, height=360)
            imagenFile2 = imutils.resize(imagenFile, height=360)
            #Visualiza la imagen en la ventana
            imageToShow = imutils.resize(imagenFile, width=370)
            imageToShow2 = imutils.resize(imagenFile, width=370)
            #33 Mostrara los colores correctos de la imagen
            #esto por que open cv lee la imagen en BGR y hay que pasarlo a RGB y PIL trabaja con RGB
            imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
            imageToShow2 = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2GRAY)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            im2 = Image.fromarray(imageToShow2)
            img2 = ImageTk.PhotoImage(image=im2)
            lblInputImagen1.configure(image=img)
            lblInputImagen1.image = img
            lblInputImagen2.configure(image=img2)
            lblInputImagen2.image = img2
    except :
        messagebox.showerror(message="El archivo seleccionado no es un tipo de imagen válido")
def boton_salir():
    ventana.destroy()

#Cuadros de las Imagenes
lblInputImagen1 = tk.Label(ventana)
lblInputImagen2 = tk.Label(ventana)
lblInputImagen1.place(x=20, y=170, width=370, height=360)
lblInputImagen1.configure(bg="red")
lblInputImagen2.place(x=400, y=170, width=370, height=360)
lblInputImagen2.configure(bg="gray")

#Botones
CImagen = tk.Button(ventana, text="Cargar Imagen", command=elegir_imagen)
CImagen.place(x=60, y=20, width=110, height=23)
salir = tk.Button(ventana, text="Salir", command=boton_salir)
salir.place(x=220, y=20, width=75, height=23)

#Labeltext
Limagen = tk.Label(ventana, text="Imagen Original")
Limagen.place(x=30, y=150, width=90, height=15)
LByN = tk.Label(ventana, text="Imagen Blanco y Negro")
LByN.place(x=410, y=150, width=130,height=15)

ventana.mainloop()