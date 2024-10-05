#------------------------------ Importamos las librerias ----------------------------------------
import cv2
import numpy as np
import SeguimientoMano as sm  # Programa que contiene la detección y seguimiento de manos
import pyautogui  # Librería que nos va a permitir manipular el mouse

#--------------------------------- Declaracion de variables ---------------------------------------
anchocam, altocam = 640, 480
cuadro = 100  # Rango donde podemos interactuar
anchopanta, altopanta = pyautogui.size()  # Obtenemos las dimensiones de nuestra pantalla
sua = 5
pubix, pubiy = 0, 0
cubix, cubiy = 0, 0

#----------------------------------- Lectura de la cámara ----------------------------------------
cap = cv2.VideoCapture(0)
cap.set(3, anchocam)  # Definimos un ancho y un alto definido para siempre
cap.set(4, altocam)

#------------------------------------ Declaramos el detector -----------------------------
detector = sm.detectorManos(maxManos=1)  # Ya que solo vamos a utilizar una mano

while True:
    #----------------- Vamos a encontrar los puntos de la mano -----------------------------
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame)  # Encontramos las manos
    lista, bbox = detector.encontrarposicion(frame)  # Mostramos las posiciones

    #----------------- Obtener la punta del dedo índice y corazón ----------------------------
    if len(lista) != 0:
        x1, y1 = lista[8][1:]  # Extraemos las coordenadas del dedo índice
        x2, y2 = lista[12][1:]  # Extraemos las coordenadas del dedo corazón

        #----------------- Comprobar que dedos están arriba --------------------------------
        dedos = detector.dedosarriba()  # Contamos con 5 posiciones nos indica si levanta cualquier dedo
        cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)  # Generamos cuadro

        #----------------- Modo movimiento: solo dedo índice -------------------------------------
        if dedos[1] == 1 and dedos[2] == 0:  # Si el índice está arriba pero el corazón está abajo
            #-----------------> Modo movimiento conversión a los píxeles de mi pantalla -------------
            x3 = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
            y3 = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))

            #------------------------------- Suavizado los valores ----------------------------------
            cubix = pubix + (x3 - pubix) / sua  # Ubicación actual = ubi anterior + x3 - Pa dividida el valor suavizado
            cubiy = pubiy + (y3 - pubiy) / sua

            #-------------------------------- Mover el Mouse ---------------------------------------
            pyautogui.moveTo(anchopanta - cubix, cubiy)  # Enviamos las coordenadas al Mouse
            cv2.circle(frame, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        #----------------------------- Comprobar si está en modo click -------------------------
        if dedos[1] == 1 and dedos[2] == 1:  # Si el índice está arriba y el corazón también
            # ---------------> Modo click: encontrar la distancia entre ellos -------------------------
            longitud, frame, linea = detector.distancia(8, 12, frame)  # Nos entrega la distancia entre el punto 8 y 12
            if longitud < 30:
                cv2.circle(frame, (linea[4], linea[5]), 10, (0, 255, 0), cv2.FILLED)

                #-------------------- Hacemos click si la distancia es corta ---------------------------
                pyautogui.click()

    cv2.imshow("Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
