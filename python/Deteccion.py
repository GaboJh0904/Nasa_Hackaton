import cv2
import os

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

cap = cv2.VideoCapture(0)  # Cambia el índice si es necesario

if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()

# Factor de escala para aumentar el tamaño de la imagen del astronauta
factor_escala = 1.5  # Puedes ajustar este valor para hacer la imagen más grande o más pequeña

while True:
    ret, frame = cap.read()
    
    if ret:  # Verificar si ha leído correctamente
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = cascadeDetector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in objects:
            # Redimensionar la imagen del astronauta al tamaño del rostro detectado
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

        cv2.imshow("Detección de rostros con astronauta", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Presionar 'ESC' para salir
            break
    else:
        print("Error: No se pudo leer el frame de la cámara")
        break

cap.release()
cv2.destroyAllWindows()
