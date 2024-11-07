import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import imutils
import cv2
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Ventana
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("Ecualizacion")

def elegir_imagen():
    try:
        path_image = filedialog.askopenfilename(filetype=[
            ("image", "jpg"),
            ("image", "jpeg"),
            ("image", "png")])
        if len(path_image) > 0:
            #Lee la imagen
            imagenFile = cv2.imread(path_image)
            imagenFile = imutils.resize(imagenFile, height=360)
            #Visualiza la imagen en la ventana
            imageToShow = imutils.resize(imagenFile, width=370)
            #Ecualiza la imagen
            gray = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2GRAY)
            equ = cv2.equalizeHist(gray)
            #Muestra la imagen ecualizada en la ventana
            equToShow = cv2.cvtColor(equ, cv2.COLOR_GRAY2RGB)
            imEq = Image.fromarray(equToShow)
            imgEq = ImageTk.PhotoImage(image=imEq)
            lblInputImagen1.configure(image=imgEq)
            lblInputImagen1.image = imgEq
            #Muestra el histograma de la imagen ecualizada
            fig, ax = plt.subplots()
            ax.hist(equ.ravel(), 256, [0,256])
            ax.set_title('Histograma ecualizado')
            canvas = FigureCanvasTkAgg(fig, master=ventana)
            canvas.draw()
            canvas.get_tk_widget().place(x=60, y=160, width=360, height=320)
            
    except :
        messagebox.showerror(message="El archivo seleccionado no es un tipo de imagen válido")
        
def boton_salir():
    ventana.destroy()

#Cuadros de las Imagenes
lblInputImagen1 = tk.Label(ventana)
lblInputImagen1.place(x=460, y=160, width=310, height=320)
lblInputImagen1.configure(bg="gray")
lblInputImagen2 = tk.Label(ventana)
lblInputImagen2.configure(bg='gray')
lblInputImagen2.place(x=60, y=160, width=360, height=320)

#Botones
CImagen = tk.Button(ventana, text="Cargar Imagen", command=elegir_imagen)
CImagen.place(x=0, y=0, width=160, height=50)
salir = tk.Button(ventana, text="Salir", command=boton_salir)
salir.place(x=170, y=0, width=110, height=50)

ventana.mainloop()