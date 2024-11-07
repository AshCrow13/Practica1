import cv2
import numpy as np
import os
import imutils

#El 0 puede cambiar dependiendo de la camara a utilizar
cap = cv2.VideoCapture(0)
haar_file = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + haar_file)
loop = True
while loop:
    (_, im) = cap.read() 
    if _ == True:
        #ENCONTRANDO CONTORNOS DE LA IMAGEN
        #Cambiar imagen de color a gris
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #Analiza los rostros en la escala de gris
        faces = face_cascade.detectMultiScale(gray)
        #Volver la imagen gris a una binaria
        _,th = cv2.threshold(gray, 140, 240, cv2.THRESH_BINARY)   
        #Los numeros cambian (menor el numero es mas blanco, mayor el numero mas oscuro)
        #Encontrar los contornos de la imagen binaria (solo encuentra en imagenes binarias)
        contornos, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Muestra 3 ventas, la imagen binaria, la imagen capturada y la imagen con contornos
        cv2.imshow('Binaria', th)
        cv2.imshow('Video', im)
        #Dentro del imshow se llama a los contornos dibujados, no hacer fuera porque no imprimiria el video sin contornos
        cv2.imshow('Contornos', cv2.drawContours(im, contornos, -1, (0,255,0), 2))
        #CONTANDO OBJETOS
        totalM = 0
        totalC = 0
        for c in contornos:
            area = cv2.contourArea(c)
            if area > 1700:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02*peri, True)
                #MESAS
                if len(approx) == 4:
                    cv2.imshow('objetos', cv2.drawContours(im, [approx], -1, (255, 0, 0), 2, cv2.LINE_AA))
                    totalM += 1
                    #CARAS
                    for(x, y, w, h) in faces:
                        cv2.rectangle(im, (x, y), (x+w , y+h), (255, 0, 0), 2)
                        totalC += 1
    cara = 'Personas: ' + str(totalC)
    mesa = 'Mesa: ' + str(totalM)
    cv2.imshow('Mesas: ', cv2.putText(im, mesa, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2))
    cv2.imshow('Personas: ', cv2.putText(im, cara, (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2))
    key = cv2.waitKey(10)
    #Presiona "q" para cerrar la aplicación
    if key  == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()