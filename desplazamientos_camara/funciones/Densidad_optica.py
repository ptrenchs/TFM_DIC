import cv2
import os
import numpy as np
from .Directorio import *

class optical_flow:
    def dense_optical_flow(ruta='',ruta_salida=''):
        if ruta == '':
            cap = cv2.VideoCapture(0)
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
                    height, width, _ = frame.shape
                    # size = (width,height)
                    fps = 30  # Cuadros por segundo
                    frame_size = (width,height)  # Tamaño del video (ancho, alto)
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    # out = cv2.VideoWriter(ruta_salida, fourcc, fps, frame_size)
                    i +=1

                frame2 = frame.copy()
                next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

                flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

                mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                hsv[...,0] = ang*180/np.pi/2
                hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
                cv2.imshow('Resoltado',rgb)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                # out.write(rgb)
            
            cap.release()
            # out.release()
            return None
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
                    height, width, _ = frame.shape
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