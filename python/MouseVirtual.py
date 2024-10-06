import cv2
import numpy as np
import SeguimientoMano as sm
import pyautogui
import webbrowser
import time

def iniciar_mouse_virtual():
    # Configuración de la cámara
    anchocam, altocam = 640, 480
    cuadro = 100
    anchopanta, altopanta = pyautogui.size()
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

    # URL del video de YouTube
    url_video = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Reemplaza con la URL del video que desees

    while True:
        ret, frame = cap.read()
        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)

        if len(lista) != 0:
            x1, y1 = lista[8][1:]  # Punta del índice
            x2, y2 = lista[12][1:]  # Punta del medio
            x3, y3 = lista[16][1:]  # Punta del anular
            x4, y4 = lista[20][1:]  # Punta del meñique

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

            # Abrir video de YouTube con un gesto específico
            if dedos[1] == 1 and dedos[2] == 1 and dedos[3] == 1:  # Índice, medio y anular arriba
                print("Abriendo video de YouTube...")
                webbrowser.open(url_video)  # Abrir el video de YouTube
                time.sleep(2)  # Esperar 2 segundos para evitar múltiples aperturas


        cv2.imshow("Mouse", frame)
        k = cv2.waitKey(1)
        if k == 27:  # Presionar 'ESC' para salir
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    iniciar_mouse_virtual()
