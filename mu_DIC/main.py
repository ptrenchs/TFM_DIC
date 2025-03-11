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




def ordenar_lista_num(lista):

    def num_inicio(nombre, fin = False):
        if fin:
            nombre = ''.join([i for i in nombre][::-1])
            for i,rt in enumerate(nombre):
                if not rt.isnumeric():
                    if nombre[:i] == '':
                        return ''
                    return int(''.join([j for j in nombre[:i]][::-1]))
                    break

        else:
            for i,rt in enumerate(nombre):
                if not rt.isnumeric():
                    if nombre[:i] == '':
                        return ''
                    return int(nombre[:i])
                    break
    
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

    lista_ordenada = []
    lista_no_ordenada = [i for i in lista]
    num = []
    for lno in lista_no_ordenada:
        _,nombre,_ = informacion_ruta(lno)
        nu = num_inicio(nombre = nombre, fin = False)
        if type(nu) == int:
            num.append(nu)

    num = sorted(num)
    for n in num:
        for lno in lista_no_ordenada:
            _,nombre,_ = informacion_ruta(lno)
            if n == num_inicio(nombre = nombre, fin = False):
                lista_ordenada.append(lno)
                lista_no_ordenada.remove(lno)
                # num.remove(n)
                # break
        # num.append(num_inicio(nombre = nombre, fin = False))

    num = []
    for lno in lista_no_ordenada:
        _,nombre,_ = informacion_ruta(lno)
        nu = num_inicio(nombre = nombre, fin = True)
        if type(nu) == int:
            num.append(nu)

    num = sorted(num)
    for n in num:
        for lno in lista_no_ordenada:
            _,nombre,_ = informacion_ruta(lno)
            if n == num_inicio(nombre = nombre, fin = True):
                lista_ordenada.append(lno)
                lista_no_ordenada.remove(lno)
                # num.remove(n)
                # break
        # num.append(num_inicio(nombre = nombre, fin = False))
    return lista_ordenada + lista_no_ordenada

def Convertir_unit8(image):
    image_show = np.clip(image, 0, 1)  # Asegurar que los valores estén entre 0 y 1
    image_show = (image_show * 255).astype(np.uint8)  # Convertir a uint8
    return image_show

def show_image_matplotlib(path, Xc1=0, Xc2=2, Yc1=0, Yc2=2):

    if os.path.isdir(path):
        ruta_carpeta = path
        archivos_carpeta = ordenar_lista_num(archivos(ruta = ruta_carpeta))
        if archivos_carpeta == []:
            return None

        ruta_img = archivos_carpeta[0]
        
    elif os.path.isdir(path):
        ruta_img = path
    image = cv2.imread(ruta_img)[::-1,:]
    # image = cv2.rotate(image, cv2.ROTATE_180)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.imshow(image, cmap='gray', origin="lower")

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


def procesado_muDIC(path, rectangulo, campo = "displacement"):

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
    # true_strain = fields.true_strain()
    viz = dic.Visualizer(fields,images=image_stack)
    
    # ruta = crear_carpeta(ruta = '/content/Resoltado')
    ruta_ = crear_carpeta(ruta_carpeta + '/Resoltado')
    ruta_carpeta_carp, _, _ = informacion_ruta(ruta = ruta_carpeta)
    ruta_carpeta_video = crear_carpeta(ruta_carpeta_carp + '/videos')
    ruta_salida = ruta_carpeta_video + '/' + os.path.basename(ruta_carpeta) + '_Resoltado' + '.mp4'

    for i in range(len(image_stack)):
        try:
            viz.show(field = campo, frame = i, ruta_save = ruta_ + '/' + f"frame_{i+1}.png")
        except:
            break
        frame = cv2.imread(ruta_ + '/' + f"frame_{i+1}.png")
        if i == 0:
            height, width, _ = frame.shape
            # size = (width,height)
            fps = 10  # Cuadros por segundo
            frame_size = (width, height)  # Tamaño del video (ancho, alto)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)
        out.write(frame)
    out.release()
    return ruta_carpeta_video
def video_to_frame(path,ips = 'all'):

    ruta_carp,nombre_arch, _ = informacion_ruta(ruta = path)
    new_ruta_carpeta = crear_carpeta(ruta_carp + '/' + nombre_arch)

    # Abrir el video
    cap = cv2.VideoCapture(path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    # Contador de frames
    frame_count = 1
    if ips == 'all':
        ips = int(fps)
    elif fps < ips:
        ips = int(fps)
    else:
        ips = int(fps/int(ips))
    num_frame = 0
    # Leer y guardar cada frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Guardar el frame
        if num_frame % ips == 0:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_filename = new_ruta_carpeta + '/' + f'frame_{frame_count}.png'
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
        num_frame += 1

    # Liberar recursos
    cap.release()
    return new_ruta_carpeta