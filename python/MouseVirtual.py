import cv2
import numpy as np
import SeguimientoMano as sm
import pyautogui
import time
import os

def iniciar_mouse_virtual():
    # Usar la ruta absoluta del clasificador
    ruta_clasificador = r'C:\Users\afar1\OneDrive\Escritorio\Nasa_Hackaton\python\rostros\faceCascade.xml'
    print(f"Buscando clasificador en: {ruta_clasificador}")

    if not os.path.isfile(ruta_clasificador):
        print("Error: El archivo faceCascade.xml no existe.")
        exit()

    cascadeDetector = cv2.CascadeClassifier(ruta_clasificador)
    if cascadeDetector.empty():
        print("Error: No se pudo cargar el clasificador de rostro.")
        exit()

    ruta_astronauta = r'C:\Users\afar1\OneDrive\Escritorio\Nasa_Hackaton\python\astronauta.png'
    if not os.path.isfile(ruta_astronauta):
        print("Error: La imagen del astronauta no se encontró.")
        exit()

    astronauta_img = cv2.imread(ruta_astronauta, cv2.IMREAD_UNCHANGED)
    if astronauta_img is None:
        print("Error: No se pudo cargar la imagen del astronauta.")
        exit()

    anchocam, altocam = pyautogui.size()  
    cuadro = 100
    anchopanta, altopanta = anchocam, altocam  
    sua = 5
    pubix, pubiy = 0, 0
    cubix, cubiy = 0, 0

    click_sostenido = False
    last_click_time = 0
    click_delay = 0.5

    cap = cv2.VideoCapture(0)
    cap.set(3, anchocam)
    cap.set(4, altocam)

    detector = sm.detectorManos(maxManos=1)

    # Variable para almacenar la distancia inicial entre el pulgar e índice
    distancia_inicial = None

    while True:
        ret, frame = cap.read()

        # Verificar si se detecta la cara
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = cascadeDetector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in objects:
            factor_escala = 1.5  
            astronauta_resized = cv2.resize(astronauta_img, (int(w * factor_escala), int(h * factor_escala)))

            astronauta_height, astronauta_width = astronauta_resized.shape[:2]
            start_x = x + int((w - astronauta_width) / 2)  
            start_y = y + int((h - astronauta_height) / 2)  

            for c in range(0, 3):
                if start_y >= 0 and start_x >= 0 and start_y + astronauta_height <= frame.shape[0] and start_x + astronauta_width <= frame.shape[1]:
                    frame[start_y:start_y + astronauta_height, start_x:start_x + astronauta_width, c] = (
                        astronauta_resized[:, :, c] * (astronauta_resized[:, :, 3] / 255.0) + 
                        frame[start_y:start_y + astronauta_height, start_x:start_x + astronauta_width, c] * 
                        (1 - (astronauta_resized[:, :, 3] / 255.0))
                    )

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)

        if len(lista) != 0:
            x1, y1 = lista[8][1:]  # Punta del índice
            x2, y2 = lista[12][1:]  # Punta del medio
            x_pulgar, y_pulgar = lista[4][1:]  # Punta del pulgar

            dedos = detector.dedosarriba()
            cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)

            # Movimiento del mouse
            if dedos[1] == 1 and dedos[2] == 0:  # Solo dedo índice arriba
                x_mouse = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
                y_mouse = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))

                cubix = pubix + (x_mouse - pubix) / sua
                cubiy = pubiy + (y_mouse - pubiy) / sua

                pyautogui.moveTo(anchopanta - cubix, cubiy)
                cv2.circle(frame, (x1, y1), 10, (0, 0, 0), cv2.FILLED)
                pubix, pubiy = cubix, cubiy

            # Gesto de Zoom con pulgar e índice
            if dedos[1] == 1 and dedos[0] == 1:  # Pulgar e índice levantados
                longitud, frame, linea = detector.distancia(4, 8, frame)  # Distancia entre pulgar e índice

                if distancia_inicial is None:
                    distancia_inicial = longitud  # Guardar la distancia inicial

                else:
                    zoom_factor = longitud / distancia_inicial  # Factor de zoom basado en la distancia
                    if zoom_factor > 1.2:  # Alejando los dedos (Zoom in)
                        pyautogui.hotkey('ctrl', '+')
                        print("Zoom in")
                        distancia_inicial = longitud  # Actualizar la distancia inicial

                    elif zoom_factor < 0.8:  # Acercando los dedos (Zoom out)
                        pyautogui.hotkey('ctrl', '-')
                        print("Zoom out")
                        distancia_inicial = longitud  # Actualizar la distancia inicial

            # Restablecer distancia inicial cuando no se detectan ambos dedos
            else:
                distancia_inicial = None

        cv2.imshow("Mouse", frame)
        cv2.resizeWindow("Mouse", anchocam, altocam)
        k = cv2.waitKey(1)
        if k == 27:  # Presionar 'ESC' para salir
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_mouse_virtual()
