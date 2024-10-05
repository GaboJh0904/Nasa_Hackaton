<template>
    <div>
      <h2>Detección de Manos</h2>
      <video ref="videoElement" autoplay></video>
      <canvas ref="canvasElement"></canvas>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HandDetector',
    mounted() {
      this.setupCamera();
      this.initOpenCV();
    },
    methods: {
      async initOpenCV() {
        try {
          // Importar el módulo WASM
          const cv = await import('opencv.js'); // Asegúrate de que la ruta sea correcta
          
          // Espera a que se inicialice el módulo
          cv.onRuntimeInitialized = () => {
            console.log('OpenCV is ready');
            this.startDetection(cv); // Inicia la detección
          };
        } catch (error) {
          console.error('Error loading OpenCV:', error);
        }
      },
      async setupCamera() {
        const video = this.$refs.videoElement;
  
        // Configurar el flujo de la cámara
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.play();
      },
      startDetection(cv) {
        const video = this.$refs.videoElement;
        const canvas = this.$refs.canvasElement;
        const ctx = canvas.getContext('2d');
  
        // Ajustar el tamaño del canvas al tamaño del video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
  
        const processFrame = () => {
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          let src = cv.imread(canvas);
          let dst = new cv.Mat();
          
          // Procesar la imagen aquí (por ejemplo, detección de manos)
          cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
          
          // Mostrar la imagen procesada en el canvas
          cv.imshow(canvas, dst);
          
          // Liberar memoria
          src.delete();
          dst.delete();
  
          requestAnimationFrame(processFrame);
        };
  
        processFrame(); // Comienza el procesamiento del video
      },
    },
  };
  </script>
  
  <style>
  video {
    display: none; /* Ocultar el video original */
  }
  
  canvas {
    border: 1px solid black; /* Opcional: borde para el canvas */
  }
  </style>
  