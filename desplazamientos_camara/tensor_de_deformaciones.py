import cv2
import numpy as np

cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame2 = cap.read()
    if not ret:
        break

    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calcular flujo óptico
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Obtener componentes del flujo óptico
    u = flow[..., 0]  # Movimiento en X
    v = flow[..., 1]  # Movimiento en Y

    # Calcular derivadas espaciales (gradientes)
    du_dx = cv2.Sobel(u, cv2.CV_64F, 1, 0, ksize=5)
    du_dy = cv2.Sobel(u, cv2.CV_64F, 0, 1, ksize=5)
    dv_dx = cv2.Sobel(v, cv2.CV_64F, 1, 0, ksize=5)
    dv_dy = cv2.Sobel(v, cv2.CV_64F, 0, 1, ksize=5)

    # Crear tensor de deformaciones D
    # D = np.stack((du_dx, du_dy, dv_dx, dv_dy), axis=-1)  # Tensor (H, W, 2, 2)
    
    D = np.stack(((du_dx, du_dy), (dv_dx, dv_dy)), axis=-1)
    print(D)
    break

    # Mostrar magnitud del tensor (opcional)
    strain = np.sqrt(du_dx**2 + dv_dy**2)  # Traza del tensor
    strain_img = cv2.normalize(strain, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imshow('Deformaciones', strain_img)

    # strain_magnitude = np.linalg.norm(D, axis=(-2, -1))  # Magnitud en cada punto (H, W)
    # strain_img = cv2.normalize(strain_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    # cv2.imshow('Magnitud de Deformaciones', strain_img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    prvs = next.copy()  # Actualizar el frame anterior

cap.release()
cv2.destroyAllWindows()
