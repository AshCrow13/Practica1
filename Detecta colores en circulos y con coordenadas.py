import cv2
import numpy as np

def dibujar(mask,color):
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 3000:
            M = cv2.moments(c)
            if (M["m00"]==0): 
                M["m00"]=1
            x = int(M["m10"]/M["m00"])
            y = int(M['m01']/M['m00'])
            nuevoContorno = cv2.convexHull(c)
            cv2.circle(frame, (x,y), 7, (0,255,0), -1)
            cv2.putText(frame,'{},{}'.format(x,y), (x+10,y), font, 0.75, (0,255,0), 1, cv2.LINE_AA)
            cv2.drawContours(frame, [nuevoContorno], 0, color, 3)

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

font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret,frame = cap.read()
    if ret == True:
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        maskAzul = cv2.inRange(frameHSV, LowAzul, HighAzul)
        maskAmarillo = cv2.inRange(frameHSV, LowAmarillo, HighAmarillo)
        maskVerde = cv2.inRange( frameHSV, LowVerde, HighVerde)
        maskRed1 = cv2.inRange(frameHSV, LowRojo1, HighRojo1)
        maskRed2 = cv2.inRange(frameHSV, LowRojo2, HighRojo2)
        maskRed = cv2.add(maskRed1, maskRed2)
        dibujar(maskAzul,(255, 0, 0))
        dibujar(maskAmarillo,(0, 255, 255))
        dibujar(maskRed,(0, 0, 255))
        cv2.imshow('maskAzul',maskAzul)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
