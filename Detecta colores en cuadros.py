import cv2
import numpy as np

# Captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Conversión a espacio de color HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definición del rango de color 
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
    
    # Creación de una máscara
    maskAzul = cv2.inRange(hsv, LowAzul, HighAzul)
    maskVerde = cv2.inRange(hsv, LowVerde, HighVerde)
    maskRojo1 = cv2.inRange(hsv, LowRojo1, HighRojo1)
    maskRojo2 = cv2.inRange(hsv, LowRojo2, HighRojo2)
    maskAmarillo = cv2.inRange(hsv, LowAmarillo, HighAmarillo)

    # Detección de contornos
    contornoAzul, _ = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornoVerde, _ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornoRojo1, _ = cv2.findContours(maskRojo1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornoRojo2, _ = cv2.findContours(maskRojo2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornoAmarillo, _ = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contornoAzul:
        if cv2.contourArea(contour) > 120:  # Filtrar contornos pequeños
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 2)

    for contour in contornoRojo1:
        if cv2.contourArea(contour) > 120:  # Filtrar contornos pequeños
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 2)

    for contour in contornoVerde:
        if cv2.contourArea(contour) > 120:  # Filtrar contornos pequeños
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 2)
    
    for contour in contornoRojo2:
        if cv2.contourArea(contour) > 120:  # Filtrar contornos pequeños
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 2)

    for contour in contornoRojo2:
        if cv2.contourArea(contour) > 120:  # Filtrar contornos pequeños
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 120, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', maskAzul)
    cv2.imshow('Mask', maskVerde)
    cv2.imshow('Mask', maskRojo1)
    cv2.imshow('Mask', maskRojo2)
    cv2.imshow('Mask', maskAmarillo)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

