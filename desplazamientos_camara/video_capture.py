import cv2
import numpy as np

# Captura de video (0 para cámara web, o poner "video.mp4" para archivo)
cap = cv2.VideoCapture(0)

while True:
    # Leer el siguiente fotograma
    ret, frame = cap.read()
    if not ret:
        break

    n = 7
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # krenel = np.ones((n,n),np.float32) / n **2
    krenel = np.array([[1.,1.,1.],[1.,-8.,1.],[1.,1.,1.]]) * -1
    gradiente_x = cv2.Sobel(frame_gray, cv2.CV_64F, 1, 0, ksize=3)  # Derivada en X
    gradiente_y = cv2.Sobel(frame_gray, cv2.CV_64F, 0, 1, ksize=3)  # Derivada en Y

    # Convertir a valores absolutos y normalizar
    gradiente_x = cv2.convertScaleAbs(gradiente_x)
    gradiente_y = cv2.convertScaleAbs(gradiente_y)

    # Sumar los gradientes para obtener el borde completo
    bordes = cv2.addWeighted(gradiente_x, 0.5, gradiente_y, 0.5, 0)
    cv2.imshow('Imagen a escala de grises', frame_gray)
    cv2.imshow('Imagen a escala de grises desemfocada', bordes)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()