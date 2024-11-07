import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import imutils
import cv2
from datetime import datetime
import os

#Variables globales
global img, Region,valor
imageToShow = None
Captura = None

#Ventana
ventana = tk.Tk()
ventana.geometry("1500x600")
ventana.title("Analisis de patrones") 

#Direccion donde se guardaran las fotos, cambiar al usar en otra pc
personPath = r'C:\Users\oicas\Documents\vscode\Practica\Tutorial 2\CapturasTuto2-10'

#Funciones
def archivo():
    try:
        # Lee la imagen
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
            imageToShow = cv2.cvtColor(imagenFile, cv2.COLOR_BGR2GRAY)
            im = Image.fromarray(imageToShow)
            img = ImageTk.PhotoImage(image=im)
            LImagen2.configure(image=img)
            LImagen2.image = img
            valor = 0
    except Exception:
        imageToShow = None

#Creación de la función cámara la que permite tomar una fotografía a través de la cámara 
# para posteriormente analizarla
#Define una variable global para mantener el estado de la cámara y la visibilidad del botón
camara_activada = False
boton_iniciar_visible = False

def camara():
    global capture, camara_activada, boton_iniciar_visible
    if not camara_activada:
        try:
            capture = cv2.VideoCapture(cv2.CAP_ANY)
            iniciar()
            camara_activada = True
            boton_iniciar_visible = True  # Mostrar el botón "Iniciar captura"
        except Exception as e:
            messagebox.showerror(message="Error al inicializar la cámara: " + str(e))
    else:
        # Si la cámara ya está activada, detén la captura y libera los recursos
        if capture is not None:
            capture.release()
            boton_iniciar_visible = False  # Ocultar el botón "Iniciar captura"
        LImagen.configure(image="")
        messagebox.showinfo(message="Cámara desactivada")
        camara_activada = False

#La funcion iniciar permite inicializar la camara para poder tomar 
# fotografias y cargarlas al programa
def iniciar():
    global capture
    if capture is not None:
        if boton_iniciar_visible:
            BCapturar.place(x=150, y=355, width=91, height=23)
        else:
            BCapturar.place_forget()
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
            messagebox.showerror(message="No se pudo capturar ningún fotograma.")

#Funcion Captura permite capturar la fotografia al presionar el boton
def Capturar():
    global valor,Captura
    camara = capture
    _, frame = camara.read()
    frame = imutils.resize(frame, height=221)
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagen.configure(image=img)
    LImagen.image = img
    Captura = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    im = Image.fromarray(Captura)
    img = ImageTk.PhotoImage(image=im)
    LImagen2.configure(image=img)
    LImagen2.image = img
    valor = 2

#Estas funciones permiten recortar la imagen a tiempo real que ha sido 
# subida o capturada con ayuda de unos sliders
def actualizar_area_recorte(_=None):
    global imageToShow, valor, Captura
    if imageToShow is not None or Captura is not None:
        x = SX.get()
        y = SY.get()
        w = SW.get()
        h = SH.get()
        # Inicializar con un valor predeterminado
        imagen_recortada = None
        if valor == 0:
            imagen_recortada = imageToShow.copy()
        else:
            imagen_recortada = Captura.copy()
            # Crear una máscara negra del mismo tamaño que la imagen original
        mascara_negra = np.zeros_like(imagen_recortada)
            # Establecer el área seleccionada
        mascara_negra[y:h, x:w] = 255
            # Superponer la imagen original con el área seleccionada
        imagen_recortada = cv2.bitwise_and(imagen_recortada, mascara_negra)
        im = Image.fromarray(imagen_recortada)
        img_recortada = ImageTk.PhotoImage(image=im)
        LImagen2.configure(image=img_recortada)
        LImagen2.image = img_recortada

# Función para recortar imagen
def recortar_imagen():
    global imageToShow, valor, Captura
    x = SX.get()
    y = SY.get()
    w = SW.get()
    h = SH.get()
    if valor == 0:
        imagen_recortada = imageToShow[y:h, x:w]
    else:
        imagen_recortada = Captura[y:h, x:w]
    # No es necesario volver a convertir de BGR a RGB aquí
    # Superponer la imagen recortada en la posición deseada
    im = Image.fromarray(imagen_recortada)
    img_recortada = ImageTk.PhotoImage(image=im)
    LImagen2.configure(image=img_recortada)
    LImagen2.image = img_recortada
    return(imagen_recortada)

#Esta funcion permite umbralizar la imagen para encontrar manchas y posteriormente entregar 
# la cantidad de manchas de la imagen, el area manchaday el % del area de la imagen 
# que tienen manchas
def rgb():
    # Recortar la imagen antes de analizar las manchas
    recortada = recortar_imagen()
    # Luego proceder con el análisis de las manchas
    #Minimos = (int(SRedI.get()), int(SGreenI.get()), int(SBlueI.get()))
    #maximos = (int(SRedD.get()), int(SGreenD.get()), int(SBlueD.get()))
    umb = int(SGray.get())
    img_mask = cv2.inRange(recortada, umb,255)
    #img_mask = cv2.inRange(recortada, Minimos, maximos)
    img_aux = 255 - img_mask
    img_mask = Image.fromarray(img_mask)
    img_mask = ImageTk.PhotoImage(image=img_mask)
    LImagenManchas.configure(image=img_mask)
    LImagenManchas.image = img_mask    
    _, bin_imagen = cv2.threshold(img_aux, umb, 255, cv2.THRESH_BINARY_INV)
    # Contar el número de píxeles con manchas
    num_pixels_con_manchas = cv2.countNonZero(bin_imagen)
    # Calcular el porcentaje de manchas
    porcentaje_manchas = 100 - (num_pixels_con_manchas / bin_imagen.size) * 100
    # Contornos
    contornos,_ = cv2.findContours(img_aux, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #contornos = cv2.findContours(img_aux, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    area = 0
    # Verificar si num_pixels_con_manchas es diferente de cero antes de dividir
    if num_pixels_con_manchas != 0:
        area = (bin_imagen.size / (num_pixels_con_manchas / bin_imagen.size))
    else:
        area = 0
    # Cantidad de contornos
    num_formas = len(contornos)
    Cadena = f"Cantidad de manchas detectada:{num_formas}\nArea Mancha: {area}\nPorcentaje de manchas:{round(porcentaje_manchas,2)}%"
    CajaTexto.configure(state='normal')
    CajaTexto.delete(1.0, tk.END)
    CajaTexto.insert(1.0, Cadena)
    CajaTexto.configure(state='disabled')
    return img_aux

#Funcion Guardar 
def guardar_imagen():
    recortada = rgb()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    tag = date_time.strftime("%d_%m_%Y_%H_%M_%S")
    #Creamos una carpeta para almacenar las imágenes en caso de que no exista.
    if not os.path.exists(personPath):
        print('Carpeta creada: ', personPath)
        os.makedirs(personPath)
    #Guardamos la imagen recortada
    cv2.imwrite(personPath + '/Imagen_recortada_' + tag + '_.jpg',255 - recortada)

# Función para cargar imágenes de la carpeta
def cargar_imagenes_carpeta():
    global img_folder, image_path, personPath
    try:
        #image_path = filedialog.askdirectory()  # Abre el diálogo para seleccionar la carpeta
        image_path = personPath
        if image_path:
            img_folder = [os.path.join(image_path, f) for f in os.listdir(image_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if not img_folder:
                messagebox.showwarning("Advertencia", "No se encontraron imágenes en la carpeta seleccionada.")
            else:
                messagebox.showinfo("Información", f"Se han cargado {len(img_folder)} imágenes de la carpeta.")
    except Exception as e:
        messagebox.showerror(message="Error al cargar las imágenes: " + str(e))

def comparar_con_imagen(descriptors_cam, img_carpeta):
    # Función para obtener coincidencia y score con una imagen específica
    orb = cv2.ORB_create()
    _, descriptors_folder = orb.detectAndCompute(img_carpeta, None)
    if descriptors_folder is None:
        return None, float('inf')  # Retornar un puntaje alto si no hay descriptores en la imagen de carpeta
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors_cam, descriptors_folder)
    if not matches:
        return None, float('inf')  # Sin coincidencias válidas
    # Calcular el score promedio
    score = sum([m.distance for m in matches]) / len(matches)
    return img_carpeta, score

def comparar_imagenes():
    global capture, img_folder, LImagenCarpeta, CajaTexto2
    umb = int(SGray.get())
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
    #img_cam_gray = cv2.cvtColor(img_cam, cv2.COLOR_BGR2GRAY)
    _, img_cam_thresh = cv2.threshold(img_cam, umb, 255, cv2.THRESH_BINARY)
    #img_cam_gray = cv2.GaussianBlur(img_cam_gray, (5, 5), 0)
    img_cam_thresh = cv2.GaussianBlur(img_cam_thresh, (5, 5), 0)
    orb = cv2.ORB_create()
    _, descriptors_cam = orb.detectAndCompute(img_cam_thresh, None)
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
            # Comparar con la imagen natural
            img_carpeta, score_natural = comparar_con_imagen(descriptors_cam, img_carpeta)
            # Comparar con la imagen umbralizada
            img_carpeta_thresh = cv2.threshold(img_carpeta, umb, 255, cv2.THRESH_BINARY)[1]
            img_carpeta, score_thresh = comparar_con_imagen(descriptors_cam, img_carpeta_thresh)            
            # Elegir la mejor coincidencia
            if score_natural < mejor_score:
                mejor_coincidencia = img_carpeta
                mejor_score = score_natural
            if score_thresh < mejor_score:
                mejor_coincidencia = img_carpeta_thresh
                mejor_score = score_thresh
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

#Agregamos la creacion de Sliders, Botones, Labels, cuadros de imagen y textos, el slider de 
# escala de gris y la finalizacion del programa
#Sliders para recorte de imagen
SX = tk.Scale(ventana, from_=0, to=300, orient='horizontal', command=actualizar_area_recorte)
SX.place(x=425,y=5, width=311)
SY = tk.Scale(ventana, from_=0, to=240, orient='vertical', command=actualizar_area_recorte)
SY.place(x=370,y=50, height=241)
SW = tk.Scale(ventana, from_=0, to=300, orient='horizontal', command=actualizar_area_recorte)
SW.place(x=425,y=295, width=311)
SW.set(300)
SH = tk.Scale(ventana, from_=0, to=240, orient='vertical', command=actualizar_area_recorte)
SH.place(x=730, y=50, height=241)
SH.set(240)

# Botones
#BRecortar = tk.Button(ventana, text="Recortar Imagen", command=recortar_imagen)
#BRecortar.place(x=520, y=350, width=110, height=23)
BGuardar = tk.Button(ventana, text="Guardar Imagen", command=guardar_imagen)
BGuardar.place(x=900, y=310, width=120, height=23)
BArchivo = tk.Button(ventana, text="Archivo", command=archivo)
BArchivo.place(x=60, y=310, width=75, height=23)
BCamara = tk.Button(ventana, text="Camara", command=camara)
BCamara.place(x=260, y=310, width=75, height=23)
BCapturar = tk.Button(ventana, text="Iniciar captura", command=Capturar)
BFormas = tk.Button(ventana, text="Buscar Formas", command=rgb)
BFormas.place(x=580,y=360,width=131,height=23)
#BPatrones = tk.Button(ventana, text="Analizar Patron", command=Analizar_Patron)
#BPatrones.place(x=1240, y=250, width=131, height=23)
BCargarImagenes = tk.Button(ventana, text="Cargar Imágenes", command=cargar_imagenes_carpeta)
BCargarImagenes.place(x=1160, y=310, width=120, height=23)
BComparar = tk.Button(ventana, text="Comparar", command=comparar_imagenes)
BComparar.place(x=1340, y=310, width=100, height=23)

# Label
LCargar = tk.Label(ventana, text="Cargar Imagen")
LCargar.place(x=160, y=310, width=81, height=16)
LUmbral = tk.Label(ventana, text="Umbralizacion")
LUmbral.place(x=420, y=353, width=125, height=16)

# Cuadros de Imagen
LImagen = tk.Label(ventana, background="gray")
LImagen.place(x=50,y=50,width=300,height=240)
LImagen2 = tk.Label(ventana, background="gray")
LImagen2.place(x=430, y=50, width=300, height=240)
LImagenManchas = tk.Label(ventana, background="gray")
LImagenManchas.place(x=810,y=50,width=300,height=240)
#LImagenPatron = tk.Label(ventana, bg="gray")
#LImagenPatron.place(x=1150,y=20,width=300,height=240)
LImagenCarpeta = tk.Label(ventana, bg="gray")
LImagenCarpeta.place(x=1150, y=50, width=300, height=240)

# Cuadro de Texto
CajaTexto = tk.Text(ventana, state="disabled")
CajaTexto.place(x=805,y=350,width=311,height=100)
CajaTexto2 = tk.Text(ventana, state="disabled")
CajaTexto2.place(x=1145,y=350,width=311,height=100)

# Spinbox
SGray = tk.Spinbox(ventana, from_=0, to=255)
SGray.place(x=460, y=380, width=45)

ventana.mainloop()