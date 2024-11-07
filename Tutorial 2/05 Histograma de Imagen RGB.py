import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from PIL import ImageTk
import imutils
import cv2
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Ventana
ventana = tk.Tk()
ventana.geometry("1400x600")
ventana.title("Grafica Histograma RGB") 

#Imagen
imagenFile = None

#Grafica Histograma RGB
def calcularHistograma(imagen):
    color = ('b','g','r')
    figure, axs = plt.subplots(1, 3, figsize=(10, 4))
    for i, c in enumerate(color):
        hist = cv2.calcHist([imagen], [i], None, [256],[0,256])
        if c == 'b':
            axs[i].plot(hist, color='blue')
        elif c == 'g':
            axs[i].plot(hist, color='green')
        else:
            axs[i].plot(hist, color='red')
        axs[i].set_xlim([0, 256])
    plt.suptitle("Histograma RGB")
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(figure, master=ventana)
    canvas.get_tk_widget().place(x=60, y=160, width=900, height=400)

#Funcion para cargar la foto
def CargarFoto():
    try:
        #Lee la imagen
        path_image = filedialog.askopenfilename(filetype=[
            ("image","jpg"),
            ("image","jpeg"),
            ("image","png")])
        if len(path_image) > 0:
            global imagenFile, img
            imagenFile = cv2.imread(path_image)
            imagenFile = imutils.resize(imagenFile, height=360)
            #Visualiza la imagen en la ventana
            imageToShow = imutils.resize(imagenFile, width=370)
            imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            lblInputImagen1.configure(image=img)
            lblInputImagen1.image = img
            calcularHistograma(imagenFile)
    except :
        messagebox.showerror(message="El archivo seleccionado no es un tipo de imagen válido")
def boton_salir():
    ventana.destroy()

#Botones
CImagen = tk.Button(ventana, text="Cargar Imagen", command=CargarFoto)
CImagen.place(x=0, y=0, width=160, height=50)
salir = tk.Button(ventana, text="Salir", command=boton_salir)
salir.place(x=280, y=0, width=110, height=50)

#Cuadros de las Imagenes
lblInputImagen1 = tk.Label(ventana,bg='gray')
lblInputImagen1.place(x=1000, y=160, width=310, height=320)

ventana.mainloop()