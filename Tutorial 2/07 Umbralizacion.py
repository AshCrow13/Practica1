import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image
from PIL import ImageTk
import imutils

#Ventana
ventana = tk.Tk()
ventana.geometry("700x500")
ventana.title("Umbralizacion")
def CargarI():
    try:
        #Lee la imagen
        path_image = filedialog.askopenfilename(filetype=[
            ("image", "jpg"),
            ("image", "jpeg"),
            ("image", "png")])
        if len(path_image) > 0:
            global U
            imagenFile = cv2.imread(path_image)
            U = cv2.imread(path_image)
            U = imutils.resize(U, width=271, height=311)
            U = cv2.cvtColor(U, cv2.COLOR_BGR2GRAY)
            imagenFile = imutils.resize(imagenFile, height=311)
            #Visualiza la imagen en la ventana
            imageToShow = imutils.resize(imagenFile, width=271)
            imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            CImagen1.configure(image=img)
            CImagen1.image = img
    except :
        messagebox.showerror(message="El archivo seleccionado no es un tipo de imagen válido")

def Umbralizar():
    valor = int(SBNumero.get())
    ret, thresh1 = cv2.threshold(U, valor, 255, cv2.THRESH_BINARY)
    Umbral = Image.fromarray(thresh1)
    Umbral = ImageTk.PhotoImage(image=Umbral)
    CImagen2.configure(image=Umbral)
    CImagen2.image = Umbral

#Boton
BCargarImagen = tk.Button(ventana, text="Cargar Imagen", command=CargarI)
BCargarImagen.place(x=50, y=50, width=91, height=23)
BUmbralizar = tk.Button(ventana, text="Umbralizar", command=Umbralizar)
BUmbralizar.place(x=350, y=50, width=75, height=23)

#SpinBox
#Si se quiere evitar que el usuario escriba numeros mayores a 255 se debe de añadir el parametro
# state="readonly dentro de tk.Spinbox"
SBNumero = tk.Spinbox(ventana, from_=0,to=255)
SBNumero.place(x=450, y=50, width=42, height=22)

#Cuadro de las Imagenes
CImagen1 = tk.Label(ventana, background="gray")
CImagen1.place(x=40, y=100, width=271, height=311)
CImagen2 = tk.Label(ventana, background="gray")
CImagen2.place(x=350, y=100, width=271, height=311)

ventana.mainloop()

