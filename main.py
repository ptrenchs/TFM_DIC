import os
from IPython.display import clear_output
import matplotlib.pyplot as plt
import matplotlib.patches as pch
import numpy as np
import cv2

try:
    import sys
    sys.path.append('/content/muDIC')
except:
    pass

import muDIC as dic
from muDIC import vlab

def show_image_matplotlib(image, Xc1=0, Xc2=2, Yc1=0, Yc2=2):
    fig, ax = plt.subplots(figsize=(5,5))
    ax.imshow(image, cmap='gray')

    # Crear rectángulo
    x, y = Xc1, Yc1  # Esquina inferior izquierda
    width, height = Xc2 - Xc1, Yc2 - Yc1

    rect = pch.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
    ax.add_patch(rect)  # Agregar el rectángulo a los ejes, no a plt

    plt.title("Imagen Generada")
    plt.show()
    return float(Xc1), float(Xc2), float(Yc1), float(Yc2)

def crear_carpeta(ruta):
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    return ruta

def informacion_ruta(ruta):
    while True:
        ruta = ruta.replace('//','/')
        if '//' not in ruta:
            break
    if ruta[-1] == '/':
        ruta = ruta[:-1]
    ruta_split = ruta.split('/')
    nombre = ruta_split[-1]
    nombre_split = nombre.split('.')
    if 1 < len(nombre_split):
        nombre = '.'.join(nombre_split[:-1])
        extension = nombre_split[-1]
    else:
        extension = ''

    if len(ruta_split) == 1:
        carpeta =''
    else:
        carpeta = '/'.join(ruta_split[:-1])

    return carpeta,nombre,extension.lower()

def archivos(ruta):
    if os.path.isdir(ruta):
        return [os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))]
    else:
        return []

# path = r"/content/muDIC/Examples/example_data" # Ruta donde se ubica les imagenes en formato ".tif"


def procesado_muDIC(path, rectangulo):

    Xc1, Xc2, Yc1, Yc2 = rectangulo
    if os.path.isdir(path):
        ruta_carpeta = path
        archivos_carpeta = archivos(ruta = ruta_carpeta)
        if archivos_carpeta == []:
            return None

        _,_,extencion = informacion_ruta(archivos_carpeta[0])
        
    elif os.path.isdir(path):
        ruta_carpeta,_,extencion = informacion_ruta(path)

    image_stack = dic.image_stack_from_folder(ruta_carpeta,file_type="." + extencion)
    mesher = dic.Mesher()
    mesh = mesher.mesh(images = image_stack, Xc1 = Xc1, Xc2 = Xc2, Yc1 = Yc1, Yc2 = Yc2, GUI=False, verbose=True)
    inputs = dic.DICInput(mesh,image_stack)
    dic_job = dic.DICAnalysis(inputs)
    results = dic_job.run()
    fields = dic.Fields(results)
    true_strain = fields.true_strain()
    viz = dic.Visualizer(fields,images=image_stack)
    
    # ruta = crear_carpeta(ruta = '/content/Resoltado')
    ruta_ = ruta_carpeta + '/Resoltado'

    ruta_salida = ruta_ + '.mp4'

    for i in range(len(image_stack)):
        viz.show(field="True strain", frame = i, ruta_save= ruta_ + '/' + f"frame_{i+1}.png")
        frame = cv2.imread(ruta_ + '/' + f"frame_{i+1}.png")
        if i == 0:
            height, width, _ = frame.shape
            # size = (width,height)
            fps = 10  # Cuadros por segundo
            frame_size = (height, width)  # Tamaño del video (ancho, alto)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)
        out.write(frame)
    out.release()

