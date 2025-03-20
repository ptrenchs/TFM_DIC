# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)
# ret, frame1 = cap.read()
# prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# while True:
#     ret, frame2 = cap.read()
#     if not ret:
#         break

#     next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

#     # Calcular flujo óptico
#     flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

#     # Obtener componentes del flujo óptico
#     u = flow[..., 0]  # Movimiento en X
#     v = flow[..., 1]  # Movimiento en Y

#     # Calcular derivadas espaciales (gradientes)
#     du_dx = cv2.Sobel(u, cv2.CV_64F, 1, 0, ksize=5)
#     du_dy = cv2.Sobel(u, cv2.CV_64F, 0, 1, ksize=5)
#     dv_dx = cv2.Sobel(v, cv2.CV_64F, 1, 0, ksize=5)
#     dv_dy = cv2.Sobel(v, cv2.CV_64F, 0, 1, ksize=5)

#     # Calcular la magnitud de la deformación (norma de Frobenius del tensor)
#     deformation_magnitude = np.sqrt(du_dx**2 + du_dy**2 + dv_dx**2 + dv_dy**2)

#     # Normalizar para visualizar en escala de grises (0-255)
#     deformation_norm = cv2.normalize(deformation_magnitude, None, 0, 255, cv2.NORM_MINMAX)
#     deformation_norm = deformation_norm.astype(np.uint8)

#     # Aplicar mapa de colores (colormap) para visualización cromática
#     deformation_colormap = cv2.applyColorMap(deformation_norm, cv2.COLORMAP_JET)

#     # Mostrar la imagen con deformación cromática
#     cv2.imshow('Deformación Cromática', deformation_colormap)

#     if cv2.waitKey(25) & 0xFF == ord('q'):
#         break

#     prvs = next.copy()  # Actualizar el frame anterior

# cap.release()
# cv2.destroyAllWindows()





import cv2
import numpy as np

def compute_optical_flow(prvs, next):
    """Calcula el flujo óptico usando el método de Farneback."""
    return cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

def compute_deformation_tensor(flow):
    """Calcula el tensor de deformaciones a partir del flujo óptico."""
    u, v = flow[..., 0], flow[..., 1]
    du_dx = cv2.Sobel(u, cv2.CV_64F, 1, 0, ksize=5)
    du_dy = cv2.Sobel(u, cv2.CV_64F, 0, 1, ksize=5)
    dv_dx = cv2.Sobel(v, cv2.CV_64F, 1, 0, ksize=5)
    dv_dy = cv2.Sobel(v, cv2.CV_64F, 0, 1, ksize=5)
    D = np.stack(((du_dx, du_dy), (dv_dx, dv_dy)), axis=-1).reshape(du_dx.shape[0], du_dx.shape[1], 2, 2)
    return D

def compute_strain_magnitude(D):
    """Calcula la magnitud de la deformación usando la norma de Frobenius."""
    return np.linalg.norm(D, axis=(-2, -1))

def compute_strain_and_rotation(D):
    """Separa el tensor en deformación pura y rotación."""
    strain = 0.5 * (D + np.transpose(D, (0, 1, 3, 2)))
    rotation = 0.5 * (D - np.transpose(D, (0, 1, 3, 2)))
    return strain, rotation

def detect_moving_objects(strain_magnitude, threshold=50):
    """Genera una máscara de objetos en movimiento según la deformación."""
    return (strain_magnitude > threshold).astype(np.uint8) * 255

def process_video():
    cap = cv2.VideoCapture(0)
    ret, frame1 = cap.read()
    prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    
    while True:
        ret, frame2 = cap.read()
        if not ret:
            break
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        flow = compute_optical_flow(prvs, next)
        D = compute_deformation_tensor(flow)
        strain_magnitude = compute_strain_magnitude(D)
        strain, rotation = compute_strain_and_rotation(D)
        moving_objects = detect_moving_objects(strain_magnitude)
        
        # Normalizar para visualización
        strain_img = cv2.normalize(strain_magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        rotation_img = cv2.normalize(np.linalg.norm(rotation, axis=(-2, -1)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Aplicar mapa de colores (colormap) para visualización cromática
        deformation_norm = cv2.normalize(strain_img, None, 0, 255, cv2.NORM_MINMAX)
        deformation_colormap = cv2.applyColorMap(deformation_norm, cv2.COLORMAP_JET)
        
        cv2.imshow('Deformacion Cromatica', deformation_colormap)
        cv2.imshow('Deformacion Pura', strain_img)
        cv2.imshow('Rotacion', rotation_img)
        cv2.imshow('Objetos en Movimiento', moving_objects)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        prvs = next.copy()
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video()

