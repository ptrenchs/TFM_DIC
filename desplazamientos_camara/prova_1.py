import cv2
import numpy as np

# Captura de video (0 para cámara web, o poner "video.mp4" para archivo)
cap = cv2.VideoCapture(0)

# Parámetros para la detección de esquinas (puntos a rastrear)
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Parámetros del algoritmo de Lucas-Kanade para el cálculo del flujo óptico
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Leer el primer fotograma
ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# Detectar esquinas iniciales (puntos a seguir)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Crear una máscara para dibujar el flujo óptico
mask = np.zeros_like(old_frame)

while True:
    # Leer el siguiente fotograma
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcular el flujo óptico con Lucas-Kanade
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Seleccionar los puntos buenos (aquellos donde se detectó movimiento)
    if p1 is not None:
        good_new = p1[st == 1]
        good_old = p0[st == 1]

        # Dibujar las líneas del flujo óptico
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
            frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 0, 255), -1)

        # Superponer el dibujo en el video
        img = cv2.add(frame, mask)

        # Mostrar el resultado
        cv2.imshow('Optical Flow - Lucas Kanade', img)

        # Actualizar los fotogramas y puntos para la siguiente iteración
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()