import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import imutils
import os
import numpy as np

# Variables globales
global capture, img_cam, img_folder, imageToShow, matched_image
imageToShow = None
img_cam = None
img_folder = None
personPath = r'C:\Users\oicas\Documents\vscode\Practica\Tutorial 2\CarpetaComparar'  # Cambia esta ruta

# Ventana principal
ventana = tk.Tk()
ventana.geometry("900x600")
ventana.title("Comparación de Imágenes")

# Función para abrir la cámara y capturar una imagen
def abrir_camara():
    global capture, img_cam
    try:
        capture = cv2.VideoCapture(0)  # Abre la cámara
        iniciar()
    except Exception as e:
        messagebox.showerror(message="Error al inicializar la cámara: " + str(e))

def iniciar():
    global capture, img_cam
    if capture is not None:
        ret, frame = capture.read()
        if ret:
            frame = imutils.resize(frame, width=300)
            ImagenCamara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(ImagenCamara)
            img_cam = ImageTk.PhotoImage(image=im)
            LImagenCam.configure(image=img_cam)
            LImagenCam.image = img_cam
            LImagenCam.after(10, iniciar)
        else:
            LImagenCam.image = ""
            capture.release()

# Función para cargar imágenes de la carpeta
def cargar_imagenes_carpeta():
    global img_folder
    try:
        image_path = filedialog.askdirectory()  # Abre el diálogo para seleccionar la carpeta
        if image_path:
            img_folder = [os.path.join(image_path, f) for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if not img_folder:
                messagebox.showwarning("Advertencia", "No se encontraron imágenes en la carpeta seleccionada.")
            else:
                messagebox.showinfo("Información", f"Se han cargado {len(img_folder)} imágenes de la carpeta.")
    except Exception as e:
        messagebox.showerror(message="Error al cargar las imágenes: " + str(e))

# Función para comparar la imagen capturada con las imágenes en la carpeta
def comparar_imagenes():
    global capture, img_folder, imageToShow, matched_image
    if img_folder is None or not img_folder:
        messagebox.showwarning("Advertencia", "Primero debes cargar una carpeta con imágenes.")
        return
    
    if capture is None or not capture.isOpened():
        messagebox.showwarning("Advertencia", "Primero debes capturar una imagen con la cámara.")
        return

    # Capturar la imagen de la cámara
    ret, img_cam = capture.read()
    if ret:
        img_cam_gray = cv2.cvtColor(img_cam, cv2.COLOR_BGR2GRAY)

        orb = cv2.ORB_create()
        keypoints_cam, descriptors_cam = orb.detectAndCompute(img_cam_gray, None)

        mejor_coincidencia = None
        mejor_score = 0

        # Comparar con cada imagen de la carpeta
        for img_path in img_folder:
            img_carpeta = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img_carpeta is not None:
                keypoints_folder, descriptors_folder = orb.detectAndCompute(img_carpeta, None)

                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(descriptors_cam, descriptors_folder)
                matches = sorted(matches, key=lambda x: x.distance)

                # Calcular la calidad de la coincidencia basada en la distancia de los descriptores
                score = sum([m.distance for m in matches]) / len(matches)

                if mejor_coincidencia is None or score < mejor_score:
                    mejor_coincidencia = img_carpeta
                    mejor_score = score

        if mejor_coincidencia is not None:
            matched_image = cv2.cvtColor(mejor_coincidencia, cv2.COLOR_GRAY2RGB)
            im = Image.fromarray(matched_image)
            img_to_show = ImageTk.PhotoImage(image=im)
            LImagenCarpeta.configure(image=img_to_show)
            LImagenCarpeta.image = img_to_show
            messagebox.showinfo("Resultado", f"Imagen más similar encontrada con un score de {mejor_score:.2f}")
        else:
            messagebox.showinfo("Resultado", "No se encontraron coincidencias.")
    else:
        messagebox.showerror(message="Error al capturar la imagen.")

# Interfaz gráfica
# Botones
BIniciarCamara = tk.Button(ventana, text="Iniciar Cámara", command=abrir_camara)
BIniciarCamara.place(x=30, y=500, width=100, height=30)

BCargarImagenes = tk.Button(ventana, text="Cargar Imágenes", command=cargar_imagenes_carpeta)
BCargarImagenes.place(x=150, y=500, width=120, height=30)

BComparar = tk.Button(ventana, text="Comparar", command=comparar_imagenes)
BComparar.place(x=300, y=500, width=100, height=30)

# Labels para mostrar las imágenes
LImagenCam = tk.Label(ventana, bg="gray")
LImagenCam.place(x=50, y=50, width=300, height=300)

LImagenCarpeta = tk.Label(ventana, bg="gray")
LImagenCarpeta.place(x=400, y=50, width=300, height=300)

# Iniciar la ventana principal
ventana.mainloop()