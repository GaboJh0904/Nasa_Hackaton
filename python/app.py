from flask import Flask, jsonify
import subprocess
import time
import os

app = Flask(__name__)

process = None  # Variable global para almacenar el proceso del mouse virtual

@app.route('/start_mouse', methods=['GET'])
def start_mouse():
    global process  # Acceder a la variable global
    try:
        # Iniciar el proceso
        process = subprocess.Popen(["python", "MouseVirtual.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Verificar si el proceso está activo
        if process.poll() is None:  # El proceso se está ejecutando
            return jsonify({"status": "Mouse virtual iniciado"})
        else:
            return jsonify({"status": "Error al iniciar el mouse virtual"})

    except Exception as e:
        return jsonify({"status": "Error al iniciar el mouse virtual", "error": str(e)})

@app.route('/stop_mouse', methods=['GET'])
def stop_mouse():
    global process  # Acceder a la variable global
    if process:
        try:
            process.terminate()  # Terminar el proceso
            process.wait()  # Esperar a que el proceso se cierre
            process = None  # Reiniciar la variable
            return jsonify({"status": "Mouse virtual detenido"})
        except Exception as e:
            return jsonify({"status": "Error al detener el mouse virtual", "error": str(e)})
    else:
        return jsonify({"status": "No hay mouse virtual en ejecución"})

if __name__ == '__main__':
    app.run(debug=True)