from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

def comparar_con_imagen(descriptors_cam, img_carpeta):
    # Función para obtener coincidencia y score con una imagen específica
    orb = cv2.ORB_create()
    keypoints_folder, descriptors_folder = orb.detectAndCompute(img_carpeta, None)
    
    if descriptors_folder is None:
        return None, float('inf')  # Retornar un puntaje alto si no hay descriptores en la imagen de carpeta

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_cam, descriptors_folder)
    if not matches:
        return None, float('inf')  # Sin coincidencias válidas
    
    # Calcular el score promedio (menor es mejor)
    score = sum([m.distance for m in matches]) / len(matches)
    return img_carpeta, score

def comparar_imagenes():
    global capture, img_folder, LImagenCarpeta, CajaTexto2
    # Verificar que existan una carpeta y una captura
    if not img_folder:
        messagebox.showwarning("Advertencia", "Primero debes cargar una carpeta con imágenes.")
        return
    if capture is None or not capture.isOpened():
        messagebox.showwarning("Advertencia", "Primero debes capturar una imagen con la cámara.")
        return

    # Capturar y procesar la imagen de la cámara
    ret, img_cam = capture.read()
    if not ret:
        messagebox.showerror("Error", "Error al capturar la imagen.")
        return

    img_cam_gray = cv2.cvtColor(img_cam, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypoints_cam, descriptors_cam = orb.detectAndCompute(img_cam_gray, None)

    if descriptors_cam is None:
        messagebox.showerror("Error", "No se encontraron características en la imagen de la cámara.")
        return

    # Inicializar la mejor coincidencia
    mejor_coincidencia = None
    mejor_score = float('inf')

    # Comparar con cada imagen de la carpeta
    for img_path in img_folder:
        img_carpeta = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img_carpeta is not None:
            img_carpeta, score = comparar_con_imagen(descriptors_cam, img_carpeta)
            if score < mejor_score:
                mejor_coincidencia = img_carpeta
                mejor_score = score

    # Mostrar resultados
    if mejor_coincidencia is not None:
        mostrar_resultado(mejor_coincidencia, mejor_score)
    else:
        messagebox.showinfo("Resultado", "No se encontraron coincidencias.")

def mostrar_resultado(mejor_coincidencia, mejor_score):
    # Función para actualizar la interfaz con la imagen encontrada
    matched_image = cv2.cvtColor(mejor_coincidencia, cv2.COLOR_GRAY2RGB)
    im = Image.fromarray(matched_image)
    img_to_show = ImageTk.PhotoImage(image=im)
    LImagenCarpeta.configure(image=img_to_show)
    LImagenCarpeta.image = img_to_show

    # Mostrar el puntaje en la interfaz
    CajaTexto2.configure(state='normal')
    CajaTexto2.delete(1.0, tk.END)
    CajaTexto2.insert(1.0, f"Imagen más similar encontrada con un score de {mejor_score:.2f}")
    CajaTexto2.configure(state='disabled')







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
            CajaTexto2.configure(state='normal')
            CajaTexto2.delete(1.0, tk.END)
            CajaTexto2.insert(1.0, f"Imagen más similar encontrada con un score de {mejor_score:.2f}")
            CajaTexto2.configure(state='disabled')
        else:
            messagebox.showinfo("Resultado", "No se encontraron coincidencias.")
    else:
        messagebox.showerror(message="Error al capturar la imagen.")