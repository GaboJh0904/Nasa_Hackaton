import cv2
import numpy as np
import SeguimientoMano as sm
import pyautogui
import time
import os

def iniciar_mouse_virtual():
    # Usar la ruta absoluta del clasificador
    ruta_clasificador = r'C:\Users\ASUS RYZEN 7\Desktop\CLASES\Nasa_Hackaton\python\rostros\faceCascade.xml'
    print(f"Buscando clasificador en: {ruta_clasificador}")

    # Verificar si el archivo existe
    if not os.path.isfile(ruta_clasificador):
        print("Error: El archivo faceCascade.xml no existe.")
        exit()

    # Cargar el clasificador en cascada
    cascadeDetector = cv2.CascadeClassifier(ruta_clasificador)

    # Verificar carga correcta
    if cascadeDetector.empty():
        print("Error: No se pudo cargar el clasificador de rostro.")
        exit()

    # Cargar la imagen del astronauta
    ruta_astronauta = r'C:\Users\ASUS RYZEN 7\Desktop\CLASES\Nasa_Hackaton\python\astronauta.png'
    if not os.path.isfile(ruta_astronauta):
        print("Error: La imagen del astronauta no se encontró.")
        exit()

    astronauta_img = cv2.imread(ruta_astronauta, cv2.IMREAD_UNCHANGED)  # Cargar con canal alfa si está disponible

    # Verificar si se cargó la imagen
    if astronauta_img is None:
        print("Error: No se pudo cargar la imagen del astronauta.")
        exit()

    # Configuración de la cámara - ajustar según la resolución de la pantalla
    anchocam, altocam = pyautogui.size()  # Usar el tamaño de la pantalla
    cuadro = 100
    anchopanta, altopanta = anchocam, altocam  # Asignar tamaño de pantalla a las variables
    sua = 5
    pubix, pubiy = 0, 0
    cubix, cubiy = 0, 0

    click_sostenido = False  # Estado para clic sostenido
    last_click_time = 0  # Tiempo del último clic
    click_delay = 0.5  # Retardo en segundos para el clic simple

    cap = cv2.VideoCapture(0)
    cap.set(3, anchocam)
    cap.set(4, altocam)

    detector = sm.detectorManos(maxManos=1)

    while True:
        ret, frame = cap.read()

        # Verificar si se detecta la cara
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = cascadeDetector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in objects:
            # Redimensionar la imagen del astronauta al tamaño del rostro detectado
            factor_escala = 1.5  # Ajusta este valor según sea necesario
            astronauta_resized = cv2.resize(astronauta_img, (int(w * factor_escala), int(h * factor_escala)))

            # Calcular las nuevas coordenadas para centrar la imagen del astronauta
            astronauta_height, astronauta_width = astronauta_resized.shape[:2]
            start_x = x + int((w - astronauta_width) / 2)  # Centrar en el eje x
            start_y = y + int((h - astronauta_height) / 2)  # Centrar en el eje y

            # Asegurarse de que el área de superposición no exceda los límites del frame
            for c in range(0, 3):  # Para los canales de BGR
                if start_y >= 0 and start_x >= 0 and start_y + astronauta_height <= frame.shape[0] and start_x + astronauta_width <= frame.shape[1]:
                    frame[start_y:start_y + astronauta_height, start_x:start_x + astronauta_width, c] = (
                        astronauta_resized[:, :, c] * (astronauta_resized[:, :, 3] / 255.0) + 
                        frame[start_y:start_y + astronauta_height, start_x:start_x + astronauta_width, c] * 
                        (1 - (astronauta_resized[:, :, 3] / 255.0))
                    )

            # Opcional: dibujar el rectángulo de detección
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)

        if len(lista) != 0:
            x1, y1 = lista[8][1:]  # Punta del índice
            x2, y2 = lista[12][1:]  # Punta del medio

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

            # Clic sostenido con movimiento
            if dedos[1] == 1 and dedos[2] == 1:  # Dedo índice y medio arriba
                longitud, frame, linea = detector.distancia(8, 12, frame)
                if longitud < 30:
                    if not click_sostenido:  # Si no se ha activado el clic sostenido
                        cv2.circle(frame, (linea[4], linea[5]), 10, (0, 255, 0), cv2.FILLED)
                        pyautogui.mouseDown()  # Presionar el botón del mouse
                        click_sostenido = True
                        print("Clic sostenido activado")  # Imprimir cuando se activa

                if click_sostenido:  # Si el clic sostenido está activo
                    x_mouse = np.interp(x1, (cuadro, anchocam - cuadro), (0, anchopanta))
                    y_mouse = np.interp(y1, (cuadro, altocam - cuadro), (0, altopanta))
                    pyautogui.moveTo(anchopanta - x_mouse, y_mouse)  # Mover el mouse
                    print("Clic sostenido en movimiento")  # Imprimir acción de movimiento

            else:
                if click_sostenido:  # Si se está levantando el dedo
                    pyautogui.mouseUp()  # Liberar el botón del mouse
                    click_sostenido = False
                    print("Clic sostenido liberado")  # Imprimir cuando se libera

            # Clic simple
            if dedos[4] == 1 and dedos[1] == 0:  # Solo dedo meñique arriba
                current_time = time.time()
                if current_time - last_click_time > click_delay:  # Verificar el retardo
                    pyautogui.click()  # Realizar clic simple
                    last_click_time = current_time  # Actualizar el tiempo del último clic
                    print("Clic simple activado")  # Imprimir acción de clic simple

        cv2.imshow("Mouse", frame)
        cv2.resizeWindow("Mouse", anchocam, altocam)  # Ajustar tamaño de la ventana
        k = cv2.waitKey(1)
        if k == 27:  # Presionar 'ESC' para salir
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_mouse_virtual()
