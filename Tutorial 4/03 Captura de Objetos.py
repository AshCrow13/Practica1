import cv2
import numpy as np
import os
import imutils
import time
from datetime import datetime

#Declaramos la variable global que nos permitirá tener acceso a nuestra cámara web. Esta 
# línea de código el parámetro elegido corresponde a la cámara web a utilizar, con un 
# valor “0” para la cámara incorporada o la primera en lista de dispositivos conectados. Para 
# cambiar esta cámara solo se debe modificar el parámetro (“1”,”2”,”3”,…N) en esta línea 
# a la correspondiente.

#El 0 puede cambiar dependiendo de la camara a utilizar
cap = cv2.VideoCapture(0) 

#Definiremos los parámetros que utilizaremos en el programa. 

haar_file = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haar_file)
count1 = 0
count2 = 0
state = False

while True:
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    date_time = datetime.fromtimestamp(timestamp)
    tag = date_time.strftime("%d_%m_%Y_%H_%M_%S")
    personPath = r'C:\Users\oicas\Documents\vscode\Practica\Tutorial 4\CapturasTuto4-03' 
    #Creamos una carpeta para almacenar las imágenes en caso de que no exista.
    if not os.path.exists(personPath):
        print('Carpeta creada: ', personPath)
        os.makedirs(personPath)
    (_, im) = cap.read()
    if _ == True:
        #Encontrando contornos de la imagen
        #Cambiar imagen de color a gris
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #Analiza los rostros en la escala de gris
        faces = face_cascade.detectMultiScale(gray)
        #Volver la imagen gris a una binaria
        _, th = cv2.threshold(gray, 140, 240, cv2.THRESH_BINARY) 
        #Los numeros cambian (menor el numero es mas blanco, mayor el numero mas oscuro)
        #Encontrar los contornos de la imagen binaria (solo encuentra en imagenes binarias)
        contornos, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Muestra 3 ventas, la imagen binaria, la imagen capturada y la imagen con contornos
        cv2.imshow('Binaria', th)
        cv2.imshow('Video', im)
        #Dentro del imshow se llama a los contornos dibujados, no hacer fuera porque no imprimiria el video sin contornos
        cv2.imshow('Contornos', cv2.drawContours(im, contornos, -1, (0,255,0), 2))
        auxFrameRec=im.copy()
        auxFrameFac=im.copy()
        #Contando objetos
        totalM = 0
        totalC = 0
        #Detecta Mesas 
        for c in contornos:
            area = cv2.contourArea(c)
            if area > 1700:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02*peri, True)            
                if len(approx) == 4:
                    cv2.imshow('objetos', cv2.drawContours(im, [approx], -1, (255, 0, 0), 2, cv2.LINE_AA))
                    totalM += 1
                    #Detecta Rostros
                    for(x, y, w, h) in faces:
                        cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        rostro = auxFrameFac[y:y+h, x:x+w]
                        rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
                        #Revisa el estado y si este es verdadero captura la foto de la cara
                        if state == True:
                            cv2.imwrite(personPath + '/Face_{}.jpg'.format(count1),rostro)                        
                        totalC += 1
                        count1 =+ 1
        #Mostramos la cuenta de objetos en una ventana.
        cara = 'Personas: '+str(totalC)
        mesa = 'Mesa: '+ str(totalM)
        cv2.imshow('Mesas: ', cv2.putText(im, mesa, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2))
        cv2.imshow('Personas: ', cv2.putText(im, cara, (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2))
        #Revisa el estado y si este es verdadero captura la imagen vista
        if state == True:
            cv2.imwrite(personPath + '/Table_'+tag+'_.jpg',auxFrameRec) 
        #Presiona "q" para salir de la aplicación
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        #Presiona "s" para cambiar el estado de la captura de imagen
        if key == ord("s"):
            if state == False:
                state = True
            else:
                state = False

cap.release()
cv2.destroyAllWindows()