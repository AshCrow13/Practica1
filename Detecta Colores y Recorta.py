import cv2
import numpy as np

cap = cv2.VideoCapture(0)

LowRojo1 = np.array([0, 100, 100], np.uint8) 
HighRojo1 = np.array([10, 255, 255], np.uint8)
LowRojo2 = np.array([170, 100, 100], np.uint8) 
HighRojo2 = np.array([180, 255, 255], np.uint8)
LowVerde = np.array([40, 100, 100], np.uint8) 
HighVerde = np.array([80, 255, 255], np.uint8)
LowAmarillo = np.array([20, 100, 100],np.uint8)
HighAmarillo = np.array([30, 255, 255],np.uint8)
LowAzul = np.array([100, 100, 100], np.uint8) 
HighAzul = np.array([140, 255, 255], np.uint8)
LowBlanco = np.array([0, 0, 200], np.uint8)
HighBlanco = np.array([180, 20, 255], np.uint8)
LowNegro = np.array([0, 0, 0], np.uint8)
HighNegro = np.array([180, 255, 50], np.uint8)

#Obtenemos los fotogramas con los que vamos a trabajar.
while True:
    ret,frame = cap.read()
    if ret==True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #Se usa la función cv2.inRange, el primer argumento es la imagen en la cual se buscará el rango, 
        # en este caso frameHSV, luego el límite inicial y final del primer rango
        maskRed1 = cv2.inRange(frameHSV, LowRojo1, HighRojo1)
        maskRed2 = cv2.inRange(frameHSV, LowRojo1, HighRojo2)
        maskRed = cv2.add(maskRed1, maskRed2)
        #Esta es una visualización adicional, en donde podremos ver el color rojo detectado, y en las 
        # regiones de la imagen donde no se presente este color se visualiza en negro
        maskRedvis = cv2.bitwise_and(frame, frame, mask= maskRed)
        #Visualizar la imagen binaria que tenemos en maskRed, para ello usamos cv2.imshow,
        # tal y como lo habíamos hecho para frame      
        cv2.imshow('frame', frame)
        cv2.imshow('maskRed', maskRed)
        cv2.imshow('maskRedvis', maskRedvis)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()