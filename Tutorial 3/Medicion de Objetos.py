import numpy as np
import cv2 

#Numpy: permite crear vectores y matrices multidimensionales, además de otras funciones matemáticas de alto nivel.
#Cv2: Computer Vision 2 es la librería encargada de permitirnos acceder a la webcam de nuestro equipo.

#Definir los parámetros y diccionario del aruco a utilizar 
parametros = cv2.aruco.DetectorParameters() 
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100) 

#El diccionario dependerá del tipo de aruco que esté utilizando, en mi caso he trabajado con un aruco 5x5 impreso
#  en un papel de 3x3cm (esta medida será importante saberla pues, nos ayudará a aproximar la distancia entre el 
# objeto y la cámara para poder medirlo correctamente), puedes generar tu propio aruco para imprimir a través de 
# la siguiente página: https://chev.me/arucogen/ aquí también podrás saber el diccionario que deberás utilizar 
# dependiendo del aruco que escojas.

#Una vez definido el aruco, con ayuda de la librería numpy crearemos los arreglos que contendrán los rangos de 
# colores que queremos que nuestra cámara detecte.

#Arreglos que contendrán los rangos de colores
LowAzul = np.array([96, 144, 106], np.uint8) 
HighAzul = np.array([124, 255, 255], np.uint8) 
LowVerde = np.array([43, 52, 106], np.uint8) 
HighVerde = np.array([91, 255, 255], np.uint8)
LowRojo1 = np.array([0, 100, 20], np.uint8) 
HighRojo1 = np.array([10, 255, 255], np.uint8)
LowRojo2 = np.array([175, 100, 20], np.uint8) 
HighRojo2 = np.array([180, 255, 255], np.uint8) 

#Por cada color debemos de crear dos arreglos en uno, pondremos el mínimo rango del color a detectar y en el otro 
# pondremos el rango máximo. Los valores de estos rangos corresponden al valor HSV de cada color

#para el color rojo debemos de declarar 4 arreglos pues, este color se encuentra tanto al principio como al 
# final del espectro.

#np.uint8: arreglo de enteros sin asignar en 8bits (de 0 a 255)

def auxNada(x):
    pass #Esta función auxiliar es la encargada de evitar que nuestro programa se caiga cuando no se registran valores.

#Crearemos una variable (cap) que almacene la información de nuestra cámara, el valor 0 indica que la cámara a utilizar 
# será la que viene por defecto con el equipo, en caso de tener más de una cámara conectada, deberá de cambiar este 
# valor a 1, 2, 3 o cualquiera sea el caso.

cap = cv2.VideoCapture(0)

while True: 
    ret, frame = cap.read() 
    if ret: 
        #Lo primero que haremos será redimensionar el tamaño de la imagen, esto lo conseguiremos haciendo uso de la 
        # función “resize()” incluída en cv2. Junto a esto, crearemos una variable en la cual almacenaremos una 
        # versión de la imagen en HSV; por defecto, las imágenes vienen en formato BGR, por lo que realizamos este 
        # cambio para manipular de manera más sencilla los colores detectados.
        frame = cv2.resize(frame, (650, 550)) 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
        #Crearemos una función llamada “medir” que recibirá como parámetros los contornos (contorno) de las figuras 
        # detectadas y la imagen (cap) en la cual debe mostrar la informaciónCrearemos una función llamada “medir” 
        # que recibirá como parámetros los contornos (contorno) de las figuras detectadas y la imagen (cap) en la 
        # cual debe mostrar la información
        #Funciones de Medidas 
        def medir(contorno, cap): 
            for c in contorno: 
                area = cv2.contourArea(c) 
                if area > 2000: 
                    rectangulo = cv2.minAreaRect(c) 
                    (x, y), (an, al), angulo = rectangulo 
                    ancho = an / proporcion_cm 
                    alto = al / proporcion_cm 
                    #cv2.circle(cap, (int(x), int(y)), 5, (255, 255, 0), -1)
                    rect = cv2.boxPoints(rectangulo) 
                    rect = np.int0(rect) 
                    cv2.polylines(cap, [rect], True, (0, 255, 255), 2) 
                    cv2.putText(cap, 'Ancho: {} cm'.format(round(ancho, 1)), (int(x), int(y-15)), cv2.LINE_AA, 0.8, (150, 0, 255), 2)
                    cv2.putText(cap, 'Alto: {} cm'.format(round(alto, 1)), (int(x), int(y+15)), cv2.LINE_AA, 0.8, (75, 0, 75), 2)
                    #Dentro de esta función se hace el cálculo de la altura y anchura del objeto el cual fue detectado, esto lo logra 
                    # a partir de los contornos que se le son entregados al momento de llamar a la función.
                    #Designar en variables la información recolectada sobre el ArUco con la función “detectMarkers()”. Una vez hecho esto, 
                    # haciendo uso de la variable “ids” crearemos un if el cual nos indicará si el aruco está o no siendo detectado, la 
                    # implementación de este condicional if es de suma importancia pues, es el que nos perimtirá mantener la cámara activa pese 
                    # a no detectar un arUco, evitando que el programa se caiga.
        #Aruco
        esquinas, ids, _ = cv2.aruco.detectMarkers(frame, diccionario, parameters=parametros) 
        #Aseguramos que el aruco sea detectado 
        if np.all(ids != None):
            esquinasInt = np.int0(esquinas) 
            cv2.polylines(frame, esquinasInt, True, (0, 0, 255), 2) 
            per_Aruco = cv2.arcLength(esquinasInt[0], True) 
            proporcion_cm = per_Aruco / 12
            #Mascaras 
            maskAzul = cv2.inRange(hsv, LowAzul, HighAzul)
            maskVerde = cv2.inRange(hsv, LowVerde, HighVerde)
            maskRojo1 = cv2.inRange(hsv, LowRojo1, HighRojo1)
            maskRojo2 = cv2.inRange(hsv, LowRojo2, HighRojo2)
            #Contornos
            contornoAzul, _ = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornoVerde, _ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornoRojo1, _ = cv2.findContours(maskRojo1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contornoRojo2, _ = cv2.findContours(maskRojo2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #Medidas
            medir(contornoAzul, frame)
            medir(contornoVerde, frame)
            medir(contornoRojo1, frame)
            medir(contornoRojo2, frame)
            #Se mencionó que el aruco empleado durante la realización de este proyecto era de 3x3cm, 
            # en esta parte del código necesitaremos conocer el área abarcada (en centímetros) por nuestro aruco pues, 
            # la variable “proporción_cm” será la encargada de, como su nombre bien lo indica, entregarle al programa 
            # la proporción en cm de los pixeles que está detectando en cada figura.
        #La función “cv2.imshow()” para mostrar en pantalla lo capturado por la cámara. Esta función 
        # recibe como primer parámetro el nombre que se le dará a la ventana contenedora del video y 
        # como segundo parámetro la imagen que deberá proyectar en la ventana.
        #Mostrar Video
        cv2.imshow('Live', frame) 
        #Cerrar el programa oprimiendo la tecla “esc”
        k = cv2.waitKey(5) 
        if k == 27:
            cv2.destroyAllWindows()
            cap.release()





