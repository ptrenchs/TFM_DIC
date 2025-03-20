from funciones import *
import os
import cv2
import time
import numpy as np
import inspect

def Convertir_unit8(image):
    image_show = np.clip(image, 0, 1)  # Asegurar que los valores estén entre 0 y 1
    image_show = (image_show * 255).astype(np.uint8)  # Convertir a uint8
    return image_show

ruta_actual = os.path.abspath(__file__)
directorio, _, _ = Directorio.informacion_ruta(ruta=ruta_actual)
ruta_img = Directorio.archivos(ruta = directorio + '/example_data')

# -------------------------------------------------------------------

# i = 0
# while i < len(ruta_img):
#     img = cv2.imread(ruta_img[i])
#     cv2.imshow('Experimento',img)

#     # Agregar una espera para que la imagen se actualice
#     cv2.waitKey(50)  # 500 milisegundos (0.5 segundos)

#     i += 1

# # Esperar una tecla para cerrar todas las ventanas al final
# cv2.destroyAllWindows()

# -------------------------------------------------------------------

def encontrar(cordenadas, valor_ref, matriz):
    i,j = cordenadas
    nxn = 1
    
    while True:
        n = int((nxn - 1) / 2)
        if i < n:
            sup_i = i
            inf_i = n + 1
        elif n <= i and  i < len(matriz) - n:
            sup_i = n
            inf_i = n + 1
        else:
            sup_i = n
            inf_i = len(matriz) - i

        if j < n:
            iz_j = j
            der_j = n + 1
        elif n <= j and  j < len(matriz[i]) - n:
            iz_j = n
            der_j = n + 1
        else:
            iz_j = n
            der_j = len(matriz[i]) - j

        start_i = i - sup_i
        stop_i = i + inf_i

        start_j = j - iz_j
        stop_j = j + der_j

        # new_matriz = [[matriz[ii][jj] for jj in range(start_j, stop_j)] for ii in range(start_i, stop_i)]
        for pi in range(start_i, stop_i):
            for pj in range(start_j, stop_j):
                if abs(np.mean(matriz[pi][pj]) - np.mean(valor_ref)):
                    return [pi,pj]
        nxn += 2
        

img_0 = cv2.imread(ruta_img[0])
img_1 = cv2.imread(ruta_img[1])

pos_inicial = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
pos_0 = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
pos_final = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
for i in range(len(img_0)):
    for j in range(len(img_0[i])):
        print([i,j])
        print([[i,j],encontrar([i,j],img_0[i][j],img_1)])












