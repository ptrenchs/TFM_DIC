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

# def encontrar(cordenadas, valor_ref, matriz):
#     i,j = cordenadas
#     nxn = 1
    
#     while True:
#         n = int((nxn - 1) / 2)
#         if i < n:
#             sup_i = i
#             inf_i = n + 1
#         elif n <= i and  i < len(matriz) - n:
#             sup_i = n
#             inf_i = n + 1
#         else:
#             sup_i = n
#             inf_i = len(matriz) - i

#         if j < n:
#             iz_j = j
#             der_j = n + 1
#         elif n <= j and  j < len(matriz[i]) - n:
#             iz_j = n
#             der_j = n + 1
#         else:
#             iz_j = n
#             der_j = len(matriz[i]) - j

#         start_i = i - sup_i
#         stop_i = i + inf_i

#         start_j = j - iz_j
#         stop_j = j + der_j

#         # new_matriz = [[matriz[ii][jj] for jj in range(start_j, stop_j)] for ii in range(start_i, stop_i)]
#         for pi in range(start_i, stop_i):
#             for pj in range(start_j, stop_j):
#                 if abs(np.mean(matriz[pi][pj]) - np.mean(valor_ref)):
#                     return [pi,pj]
#         nxn += 2
        

# img_0 = cv2.imread(ruta_img[0])
# img_1 = cv2.imread(ruta_img[1])

# pos_inicial = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
# pos_0 = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
# pos_final = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
# for i in range(len(img_0)):
#     for j in range(len(img_0[i])):
#         print([i,j])
#         print([[i,j],encontrar([i,j],img_0[i][j],img_1)])

# -------------------------------------------------------------------

import cv2
import numpy as np

def encontrar(cordenadas, valor_ref, matriz):
    i,j = cordenadas
    if matriz[i][j] == valor_ref:
        return [i,j]
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
        # print(matriz[i][j])

        submatriz = np.abs(matriz[start_i:stop_i, start_j:stop_j] - valor_ref)

        val_min = np.min(submatriz)
        if val_min < 2:
            pos = np.where(submatriz == val_min)
            modulo = []
            for i in range(len(pos[0])):
                modulo.append(abs(pos[0][i] - sup_i + 1j * (pos[1][i] - iz_j)))
            pos_pos = np.where(np.array(modulo) == np.min(modulo))
            pos_pos = pos_pos[0][0]
            pi,pj = i + (pos[0][pos_pos] - sup_i), j + (pos[1][pos_pos] - iz_j)
            # print(matriz[start_i:stop_i, start_j:stop_j])
            # print(valor_ref)
            # print([int(pi),int(pj)])
            return [int(pi),int(pj)]
        # if 7 <= nxn:
        #     return [i,j]
        nxn += 2

ruta = './Experimento_virtual_500x500'
lista_imagenes = Directorio.archivos(ruta = ruta)

ruta_save = Directorio.crear_carpeta(os.path.join('./',os.path.basename(ruta) + '_resultados'))

img_0 = np.mean(cv2.imread(lista_imagenes[0]), axis=2)
posiciones = [[[i,j] for j in range(len(img_0[i]))]for i in range(len(img_0))]
# cv2_imshow(img_0)
# for k in range(len(lista_imagenes)):
for k in range(50):
    img_1 = np.mean(cv2.imread(lista_imagenes[k]), axis=2)
    new_img = []

    # pos_inicial = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
    # pos_0 = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
    # pos_final = [[[i,j] for j in range(len(img_0[i]))] for i in range(len(img_0))]
    # len_frame = len(img_0)

    for i in range(len(img_0)):
        new_img.append([])
        for j in range(len(img_0[i])):
            # print([i,j])
            # print([[i,j],encontrar([i,j],img_0[i][j],img_1)])
            old_pos = [i,j]
            new_pos = encontrar([i,j],img_0[i][j],img_1)
            new_img[i].append(abs(old_pos[0] - new_pos[0] - 1j * (old_pos[1] - new_pos[1])))
            # if old_pos == new_pos:
            #     new_img[i].append([255 for i in range(3)])
            #     # posiciones[i][j] = 0  # no correcto

            # else:
            #     new_img[i].append([0 for i in range(3)])
            #     posiciones[old_pos[0]][old_pos[1]] = old_pos
            #     posiciones[new_pos[0]][new_pos[1]] = old_pos
            # print(new_img[i][-1])

        # print(f'{i}/{len_frame}'
    new_img = np.array(new_img)

    # Calculamos la media y la desviación estándar
    media = np.mean(new_img)
    std = np.std(new_img)

    # Definimos los límites del intervalo de confianza del 95%
    limite_inferior = media - 1.96 * std
    limite_superior = media + 1.96 * std

    # Reemplazamos los valores fuera del intervalo por 0
    new_img = np.where((new_img < limite_inferior) | (new_img > limite_superior), 0, new_img)

    new_img = (new_img * 255 / np.max(new_img)).astype(np.uint8)
    # print(new_img)
    new_img = cv2.applyColorMap(new_img, cv2.COLORMAP_JET)

    # cv2_imshow(new_img)
    cv2.imwrite(os.path.join(ruta_save,f'frame_{k}.png'), new_img)
    # cv2_imshow(img_1)
    img_0 = img_1.copy()

posiciones = np.array(posiciones)








