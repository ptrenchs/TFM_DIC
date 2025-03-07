import os
import numpy as np
import cv2
# import pandas as pd
# import matplotlib.pyplot as plt
# from math import isnan
# import scipy.stats as stats

# import shutil


# --------------------------------------------------------

class  Directorio:

    def __init__(self, rutas):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas

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
        
        # def Directorio.informacion_ruta(ruta):
        #     while True:
        #         ruta = ruta.replace('//','/')
        #         if '//' not in ruta:
        #             break
        #     if ruta[-1] == '/':
        #         ruta = ruta[:-1]
        #     ruta_split = ruta.split('/')
        #     nombre = ruta_split[-1]
        #     nombre_split = nombre.split('.')
        #     if 1 < len(nombre_split):
        #         nombre = '.'.join(nombre_split[:-1])
        #         extension = nombre_split[-1]
        #     else:
        #         extension = ''

        #     if len(ruta_split) == 1:
        #         carpeta =''
        #     else:
        #         carpeta = '/'.join(ruta_split[:-1])

        #     return carpeta,nombre,extension.lower()

        lista_ordenada = []
        lista_no_ordenada = [i for i in lista]
        num = []
        for lno in lista_no_ordenada:
            _,nombre,_ = Directorio.informacion_ruta(lno)
            nu = num_inicio(nombre = nombre, fin = False)
            if type(nu) == int:
                num.append(nu)

        num = sorted(num)
        for n in num:
            for lno in lista_no_ordenada:
                _,nombre,_ = Directorio.informacion_ruta(lno)
                if n == num_inicio(nombre = nombre, fin = False):
                    lista_ordenada.append(lno)
                    lista_no_ordenada.remove(lno)
                    # num.remove(n)
                    # break
            # num.append(num_inicio(nombre = nombre, fin = False))

        num = []
        for lno in lista_no_ordenada:
            _,nombre,_ = Directorio.informacion_ruta(lno)
            nu = num_inicio(nombre = nombre, fin = True)
            if type(nu) == int:
                num.append(nu)

        num = sorted(num)
        for n in num:
            for lno in lista_no_ordenada:
                _,nombre,_ = Directorio.informacion_ruta(lno)
                if n == num_inicio(nombre = nombre, fin = True):
                    lista_ordenada.append(lno)
                    lista_no_ordenada.remove(lno)
                    # num.remove(n)
                    # break
            # num.append(num_inicio(nombre = nombre, fin = False))
        return lista_ordenada + lista_no_ordenada

    def archivos(ruta):
        if os.path.isdir(ruta):
            return Directorio.ordenar_lista_num([os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))])
        else:
            return []
    
    def carpetas(ruta):
        if os.path.isdir(ruta):
            return Directorio.ordenar_lista_num([os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, item))])
        else:
            return []
    
    def all_archivos(self):
        archivos_all = []
        lista = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                archivos_all += Directorio.archivos(ruta=ruta)
                lista += Directorio.carpetas(ruta=ruta)
            rutas = lista
            lista = []
        return archivos_all
    
    def all_carpetas(self):
        carpetas_all = []
        lista = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                lista += Directorio.carpetas(ruta=ruta)
            rutas = lista
            carpetas_all += lista
            lista = []
        return carpetas_all
    def crear_carpeta(ruta):
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        return ruta
    
class Filtros_formato:
    def __init__(self, rutas, formatos= ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(formatos)==str:
             formatos = (formatos.replace(' ','').replace('\t','').replace('.','')).split(',')
        self.formatos = formatos
    

    def elejir(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in self.formatos:
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        new_lista.append(ruta)
                        break
            return new_lista
    
    def eliminar(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in self.formatos:
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        break
                if not (formato_ruta.lower() == formato.lower()):
                    new_lista.append(ruta)
            return new_lista


class Filtros_carpetas:

    def __init__(self, rutas, carpetas = ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(carpetas)==str:
             carpetas = (carpetas.replace(' ','').replace('\t','')).split(',')
        self.carpetas = carpetas


    def elejir(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in self.carpetas:
                    if '/' + carpeta +'/' in ruta:
                        new_lista.append(ruta)
                        break
            return new_lista
        
    def eliminar(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in self.carpetas:
                    if '/' + carpeta +'/' in ruta:
                        break

                if '/' + carpeta +'/' not in ruta:
                    new_lista.append(ruta)
            return new_lista
        
    
        
class Filtros_archivos:

    def __init__(self, rutas, archivos = ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(archivos)==str:
             archivos = (archivos.replace(' ','').replace('\t','')).split(',')
        self.archivos = archivos

    def elejir(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in self.archivos:
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        new_lista.append(ruta)
                        break
            return new_lista
    
    def eliminar(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in self.archivos:
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        break
                if not (nombre_archivo == arch):
                    new_lista.append(ruta)
            return new_lista
        
class optical_flow:
    def dense_optical_flow(ruta,ruta_salida=''):
        if ruta_salida == '':
            ruta_cap,nombre_arch,_ = Directorio.informacion_ruta(ruta = ruta)
            ruta_cap = Directorio.crear_carpeta(ruta=ruta_cap + '/Videos')
            ruta_salida = ruta_cap + '/' + nombre_arch + '_Resultado.mp4'
        else:
            ruta_cap,nombre_arch,_ = Directorio.informacion_ruta(ruta = ruta_salida)
            ruta_salida = ruta_cap + '/' + nombre_arch + '_Resultado.mp4'
        if os.path.isdir(ruta):

            lista_img = Filtros_formato(rutas = Directorio.archivos(ruta = ruta), formatos= 'png,tif,tiff').elejir()
            for i,img in enumerate(lista_img):

                img_gris = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
                # cv2_imshow(img_gris)
                if i == 0:
                    img_1 = img_gris
                    hsv = np.zeros_like(cv2.imread(img))
                    hsv[...,1] = 255
                    height, width, _ = cv2.imread(img).shape
                    # size = (width,height)
                    fps = 30  # Cuadros por segundo
                    frame_size = (width,height)  # Tamaño del video (ancho, alto)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)


                img_2 = img_gris
                flow = cv2.calcOpticalFlowFarneback(img_1,img_2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
                # cv2_imshow(rgb)
                out.write(rgb)
                img_1 = img_2

            out.release()


        elif os.path.isfile(ruta):

            cap = cv2.VideoCapture(ruta)
            i = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if i == 0:
                    frame1 = frame.copy()
                    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
                    hsv = np.zeros_like(frame1)
                    hsv[...,1] = 255
                    height, width, _ = cv2.imread(img).shape
                    # size = (width,height)
                    fps = 30  # Cuadros por segundo
                    frame_size = (width,height)  # Tamaño del video (ancho, alto)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)
                    i +=1

                frame2 = frame.copy()
                next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

                flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
                out.write(rgb)
            
            cap.release()
            out.release()
            # cv2.destroyAllWindows()
    
    def Lucas_Kanade(ruta,ruta_salida = ''):
        if ruta_salida == '':
            ruta_cap,nombre_arch,_ = Directorio.informacion_ruta(ruta = ruta)
            ruta_cap = Directorio.crear_carpeta(ruta=ruta_cap + '/Videos')
            ruta_salida = ruta_cap + '/' + nombre_arch + '_Resultado.mp4'
        else:
            ruta_cap,nombre_arch,_ = Directorio.informacion_ruta(ruta = ruta_salida)
            ruta_salida = ruta_cap + '/' + nombre_arch + '_Resultado.mp4'

        # params for ShiTomasi corner detection
        feature_params = dict( maxCorners = 100,
                            qualityLevel = 0.3,
                            minDistance = 7,
                            blockSize = 7 )

        # Parameters for lucas kanade optical flow
        lk_params = dict( winSize  = (15,15),
                        maxLevel = 2,
                        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # Create some random colors
        color = np.random.randint(0,255,(100,3))

        if os.path.isdir(ruta):
                
            lista_img = Filtros_formato(rutas = Directorio.archivos(ruta = ruta), formatos= 'png,tif,tiff').elejir()

            for i,fram in enumerate(lista_img):
                frame = cv2.imread(fram)
                if i ==0:
                    # Take first frame and find corners in it
                    # ret, old_frame = cap.read()
                    old_frame = frame.copy()
                    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
                    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

                    # Create a mask image for drawing purposes
                    mask = np.zeros_like(old_frame)

                    height, width, _ = cv2.imread(img).shape
                    # size = (width,height)
                    fps = 30  # Cuadros por segundo
                    frame_size = (width,height)  # Tamaño del video (ancho, alto)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)

                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # calculate optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

                # Select good points
                good_new = p1[st==1]
                good_old = p0[st==1]

                # draw the tracks
                for i,(new,old) in enumerate(zip(good_new,good_old)):
                    a,b = new.ravel()
                    c,d = old.ravel()

                    a, b = int(a), int(b)
                    c, d = int(c), int(d)

                    mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
                    frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
                img = cv2.add(frame,mask)

                # cv2_imshow(img)
                out.write(img)
                # Now update the previous frame and previous points
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1,1,2)

            out.release()
        elif os.path.isfile(ruta):

            cap = cv2.VideoCapture(ruta)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if i ==0:
                    # Take first frame and find corners in it
                    # ret, old_frame = cap.read()
                    old_frame = frame.copy()
                    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
                    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

                    # Create a mask image for drawing purposes
                    mask = np.zeros_like(old_frame)

                    height, width, _ = cv2.imread(img).shape
                    # size = (width,height)
                    fps = 30  # Cuadros por segundo
                    frame_size = (width,height)  # Tamaño del video (ancho, alto)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)

                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # calculate optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

                # Select good points
                good_new = p1[st==1]
                good_old = p0[st==1]

                # draw the tracks
                for i,(new,old) in enumerate(zip(good_new,good_old)):
                    a,b = new.ravel()
                    c,d = old.ravel()

                    a, b = int(a), int(b)
                    c, d = int(c), int(d)

                    mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
                    frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
                img = cv2.add(frame,mask)

                # cv2_imshow(img)
                out.write(img)
                # Now update the previous frame and previous points
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1,1,2)
            cap.release()
            out.release()
    