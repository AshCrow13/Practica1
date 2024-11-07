import os
import cv2

def procesar_imagen(imagen):
    # Aquí puedes realizar cualquier operación con la imagen
    print(f"Tamaño de la imagen: {imagen.shape}")  # Imprime el tamaño de la imagen

def mostrar_imagenes(carpeta):
    # Extensiones de imagen comunes
    extensiones = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    
    for archivo in os.listdir(carpeta):
        if any(archivo.lower().endswith(ext) for ext in extensiones):
            ruta_imagen = os.path.join(carpeta, archivo)
            imagen = cv2.imread(ruta_imagen)
            
            if imagen is not None:
                cv2.imshow(archivo, imagen)
                cv2.waitKey(0)  # Espera hasta que se presione una tecla
                procesar_imagen(imagen)  # Llama a la función para procesar la imagen
                cv2.destroyAllWindows()  # Cierra la ventana de la imagen

if __name__ == "__main__":
    ruta_carpeta = r'C:\Users\oicas\Documents\vscode\Practica\Tutorial 2\CapturasTuto2-10'  # Cambia esta ruta a tu carpeta de imágenes
    mostrar_imagenes(ruta_carpeta)
