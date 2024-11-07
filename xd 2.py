import cv2
import os
import numpy as np
from datetime import datetime

# Ruta de la carpeta donde se guardarán las imágenes
output_folder = "imagenes_procesadas"
os.makedirs(output_folder, exist_ok=True)

# Captura de imagen y procesamiento
def capturar_y_procesar_imagen(capture):
    ret, img = capture.read()
    if not ret:
        print("Error al capturar la imagen.")
        return None

    # Convertir a escala de grises y umbralizar (binarizar)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # Recortar la región de interés (ROI)
    x, y, w, h = 50, 50, 300, 300  # Ajusta las coordenadas según tus necesidades
    img_crop = img_thresh[y:y+h, x:x+w]

    # Guardar la imagen procesada
    filename = os.path.join(output_folder, f"imagen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    cv2.imwrite(filename, img_crop)
    print(f"Imagen guardada como {filename}")
    return img_crop

# Comparación de imágenes
def comparar_imagenes(capture):
    ret, img_cam = capture.read()
    if not ret:
        print("Error al capturar la imagen.")
        return None

    # Procesar la imagen de la cámara para comparación
    img_cam_gray = cv2.cvtColor(img_cam, cv2.COLOR_BGR2GRAY)
    _, img_cam_thresh = cv2.threshold(img_cam_gray, 127, 255, cv2.THRESH_BINARY)

    # Parámetros de ORB
    orb = cv2.ORB_create()
    kp_cam, des_cam = orb.detectAndCompute(img_cam_thresh, None)

    # Inicializar la mejor coincidencia
    mejor_coincidencia = None
    mejor_porcentaje = 0.0

    # Comparar con cada imagen en la carpeta
    for img_file in os.listdir(output_folder):
        img_path = os.path.join(output_folder, img_file)
        img_folder = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if img_folder is None:
            continue

        kp_folder, des_folder = orb.detectAndCompute(img_folder, None)

        if des_folder is not None:
            # Matcher de fuerza bruta con descriptores ORB
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des_cam, des_folder)
            if matches:
                # Calcular el porcentaje de similitud
                good_matches = [m for m in matches if m.distance < 50]
                porcentaje_similitud = (len(good_matches) / len(matches)) * 100

                if porcentaje_similitud > mejor_porcentaje:
                    mejor_porcentaje = porcentaje_similitud
                    mejor_coincidencia = img_folder

    if mejor_coincidencia is not None:
        print(f"Imagen más similar encontrada con {mejor_porcentaje:.2f}% de exactitud")
        cv2.imshow("Imagen más similar", mejor_coincidencia)
    else:
        print("No se encontraron coincidencias.")

# Programa principal
def main():
    # Iniciar captura de video
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("No se pudo acceder a la cámara.")
        return

    while True:
        print("\n1. Capturar y procesar imagen")
        print("2. Comparar con imágenes en la carpeta")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            capturar_y_procesar_imagen(capture)
        elif opcion == '2':
            comparar_imagenes(capture)
        elif opcion == '3':
            break
        else:
            print("Opción inválida. Intente de nuevo.")

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
