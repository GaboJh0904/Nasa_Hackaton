<template>
  <div id="app">
    <header class="header-container">
      <button class="nav-button" @click="goBack">⬅ Atrás</button>
      <h1>Planeta Jupiter</h1>
      <button class="nav-button" @click="toggleRotation">{{
          isRotating ? 'Detener Rotación' : 'Reanudar Rotación'
        }}
      </button>
    </header>

    <div class="main-content">
      <div class="container">
        <aside class="sidebar">
          <h2>Información del Planeta Júpiter</h2>
          <div class="info-section">
            <p><strong>Nombre:</strong> Júpiter</p>
            <p><strong>Radio:</strong> 69,911 km</p>
            <p><strong>Masa:</strong> 1.898 × 10<sup>27</sup> kg</p>
            <p><strong>Temperatura Promedio:</strong> -108 °C</p>
            <p><strong>Satélites Naturales:</strong> 79 (incluyendo Io y Europa)</p>
            <p><strong>Distancia Promedio al Sol:</strong> 778.5 millones de km</p>
            <p><strong>Tiempo de Rotación:</strong> 9 horas y 56 minutos</p>
            <p><strong>Tiempo de Traslación:</strong> 11.86 años terrestres</p>
            <p><strong>Composición de la Atmósfera:</strong></p>
            <ul>
              <li>Hidrógeno: 90%</li>
              <li>Helio: 10%</li>
              <li>Metano, amoníaco y vapor de agua: trazas</li>
            </ul>
            <p><strong>Descripción:</strong> Júpiter es el planeta más grande del sistema solar y un gigante gaseoso. Su atmósfera está compuesta principalmente de hidrógeno y helio, y presenta bandas de nubes y una famosa tormenta llamada la Gran Mancha Roja.</p>
            <p><strong>Origen:</strong> Júpiter se formó hace aproximadamente 4.5 mil millones de años y ha mantenido su composición primordial, lo que lo convierte en un objeto de gran interés para los científicos que estudian la formación del sistema solar.</p>
            <p><strong>Geología:</strong> Como gigante gaseoso, Júpiter no tiene una superficie sólida definida. Se cree que posee un núcleo rocoso rodeado por un manto de hidrógeno metálico, que genera un fuerte campo magnético.</p>
            <p><strong>Lunas Notables:</strong> Júpiter tiene 79 lunas conocidas, de las cuales Io, Europa, Ganimedes y Calisto son las más grandes. Io es famosa por su actividad volcánica, mientras que Europa es considerada uno de los lugares más prometedores en la búsqueda de vida extraterrestre debido a su océano subsuperficial.</p>
          </div>

          <h3>Satélites de Júpiter</h3>
          <ul>
            <li v-for="(satellite, index) in satellites" :key="index" @click="showSatelliteInfo(satellite)">
              Satélite {{ satellite.name }} - Radio Órbita: {{ satellite.orbitRadius.toFixed(2) }} km
            </li>
          </ul>

          <p>Júpiter, con su inmensa gravedad y campo magnético, juega un papel importante en la dinámica del sistema solar. Su estudio proporciona información valiosa sobre la formación y evolución de los planetas.</p>
          <p>La exploración de Júpiter y sus lunas es un objetivo primordial para las misiones espaciales, y futuros estudios podrían revelar más sobre su atmósfera y la posibilidad de vida en sus lunas.</p>

          <h3>Galería de Imágenes</h3>
          <div class="carousel">
            <div class="carousel-images" :style="{ transform: `translateX(-${currentImageIndex * 100}%)` }">
              <img v-for="(image, index) in images" :key="index" :src="image" :alt="'Imagen de Júpiter ' + (index + 1)" />
            </div>
            <button @click="prevImage" class="carousel-button">◀</button>
            <button @click="nextImage" class="carousel-button">▶</button>
          </div>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
          <br>
        </aside>
        <div class="content">


          <main class="interaction-area">
            <div ref="canvasContainer" class="canvas-container"></div>
          </main>
        </div>

        <div v-if="selectedSatellite" class="modal">
          <div class="modal-content">
            <span class="close" @click="closeModal">&times;</span>
            <h2>Información del Satélite</h2>
            <p><strong>Nombre:</strong> {{ selectedSatellite.name }}</p>
            <p><strong>Propósito:</strong> {{ selectedSatellite.purpose }}</p>
            <p><strong>Altura de la órbita:</strong> {{ selectedSatellite.orbitRadius }} km</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <ChatAssistantJupiter />
</template>

<script>
import * as THREE from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";
import earthTexture from "@/assets/jupiter.jpg"; // Textura del planeta Tierra
import image1 from "@/assets/jupiter_1.jpg";
import image2 from "@/assets/jupiter_2.png";
import ChatAssistantJupiter from "@/views/planets/jupiter/ChatAssistantJupiter.vue";

export default {
  name: "App",
  components: {
    ChatAssistantJupiter,
  },
  data() {
    return {
      isRotating: true,
      satellites: [
        { name: 'Io', orbitRadius: 4217.00, purpose: 'Satélite natural, geológicamente activo con volcanes', inclination: 0.04 },
        { name: 'Europa', orbitRadius: 6711.00, purpose: 'Satélite natural, conocido por su superficie de hielo y la posibilidad de un océano subsuperficial', inclination: 0.47 },
      ],
      heatMapTexture: null, // Textura de las áreas de calor
      heatSpots: [], // Zonas de calor
      selectedSatellite: null,
      satelliteObjects: [],
      images: [
        image1, // Reemplaza con la URL de la imagen 1
        image2, // Reemplaza con la URL de la imagen 2
        // Añade más imágenes si lo deseas
      ],
      currentImageIndex: 0,
    };
  },
  mounted() {
    this.createEarth();
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    nextImage() {
      this.currentImageIndex = (this.currentImageIndex + 1) % this.images.length;
    },
    prevImage() {
      this.currentImageIndex = (this.currentImageIndex - 1 + this.images.length) % this.images.length;
    },
    showSatelliteInfo(satellite) {
      // Lógica para mostrar información del satélite
      alert(`Información sobre ${satellite.name}`);
    },
    createEarth() {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 3;

      const renderer = new THREE.WebGLRenderer({alpha: true});
      renderer.setSize(window.innerWidth, window.innerHeight);
      this.$refs.canvasContainer.appendChild(renderer.domElement);

      // Crear la esfera de la Tierra con su textura
      const earthGeometry = new THREE.SphereGeometry(1, 32, 32);
      const textureLoader = new THREE.TextureLoader();
      const earthMaterial = new THREE.MeshBasicMaterial({
        map: textureLoader.load(earthTexture),
      });
      const earth = new THREE.Mesh(earthGeometry, earthMaterial);
      scene.add(earth);

      // Crear la textura para las áreas calientes
      this.createHeatMap(scene, earth);

      // Crear satélites
      this.createSatellites(scene);

      // Controles de cámara
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.25;
      controls.enableZoom = true;

      // Animación principal
      const animate = () => {
        requestAnimationFrame(animate);
        if (this.isRotating) {
          earth.rotation.y += 0.01;
          if (this.satelliteObjects.length) {
            this.animateSatellites(); // Animar los satélites solo si están inicializados
            this.updateHeatMapTexture(); // Actualizar textura de las áreas calientes
          }
        }
        controls.update();
        renderer.render(scene, camera);
      };
      animate();

      window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });
    },

    createHeatMap(scene, earth) {
      // Crear un canvas para representar las áreas de calor
      const heatMapCanvas = document.createElement("canvas");
      heatMapCanvas.width = 512;
      heatMapCanvas.height = 512;
      const ctx = heatMapCanvas.getContext("2d");

      // Crear la textura del mapa de calor a partir del canvas
      this.heatMapTexture = new THREE.CanvasTexture(heatMapCanvas);

      // Crear un material que combine la textura del planeta y las áreas calientes
      const heatMapMaterial = new THREE.MeshBasicMaterial({
        map: this.heatMapTexture,
        transparent: true,
      });

      // Aplicar la textura de calor directamente sobre la misma esfera de la Tierra
      const heatMapGeometry = earth.geometry; // Reutilizar la geometría de la Tierra
      const heatMapMesh = new THREE.Mesh(heatMapGeometry, heatMapMaterial);
      earth.add(heatMapMesh);

      // Definir focos de calor en varias regiones del planeta
      this.heatSpots = [
        {lat: -3.4653, lon: -62.2159, radius: 30, intensity: 0.6}, // Amazonas
        {lat: -25.2744, lon: 133.7751, radius: 25, intensity: 0.8}, // Australia
        {lat: 1.2921, lon: 36.8219, radius: 20, intensity: 0.4}, // África central
        {lat: 40.4637, lon: -3.7492, radius: 20, intensity: 0.5}, // España
        {lat: -11.2027, lon: 17.8739, radius: 15, intensity: 0.7}, // Angola
      ];
    },

    updateHeatMapTexture() {
      const ctx = this.heatMapTexture.image.getContext("2d");

      // Limpiar el lienzo
      ctx.clearRect(0, 0, 512, 512);

      // Dibujar las áreas calientes (simulando llamas)
      this.heatSpots.forEach((spot) => {
        const {x, y} = this.convertLatLonToCanvasCoords(spot.lat, spot.lon);

        // Crear un gradiente radial que simula el efecto de las llamas
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, spot.radius);
        gradient.addColorStop(0, `rgba(255, 69, 0, ${Math.random() * spot.intensity})`);
        gradient.addColorStop(1, "rgba(255, 69, 0, 0)");

        ctx.beginPath();
        ctx.arc(x, y, spot.radius, 0, 2 * Math.PI);
        ctx.fillStyle = gradient;
        ctx.fill();
      });

      // Marcar la textura como actualizada para renderizar el nuevo frame
      this.heatMapTexture.needsUpdate = true;
    },

    convertLatLonToCanvasCoords(lat, lon) {
      const x = ((lon + 180) / 360) * 512;
      const y = ((90 - lat) / 180) * 512;
      return {x, y};
    },

    createSatellites(scene) {
      const satelliteSize = 0.05; // Tamaño de los satélites

      this.satellites.forEach((satellite, index) => {
        // Calcular el radio de la órbita
        const orbitRadius = (satellite.orbitRadius + 6371) / 6371; // Añadir el radio de la Tierra (6371 km) y normalizar

        // Crear la trayectoria punteada para la órbita
        const orbitPoints = new THREE.BufferGeometry();
        const points = [];

        for (let i = 0; i <= 64; i++) {
          const angle = (i / 64) * Math.PI * 2;
          const x = Math.cos(angle) * orbitRadius;
          const y = Math.sin(angle) * orbitRadius * Math.cos(THREE.MathUtils.degToRad(satellite.inclination));
          const z = Math.sin(angle) * orbitRadius * Math.sin(THREE.MathUtils.degToRad(satellite.inclination));
          points.push(new THREE.Vector3(x, y, z));
        }

        orbitPoints.setFromPoints(points);
        const orbitMaterial = new THREE.LineDashedMaterial({color: 0x888888, dashSize: 0.05, gapSize: 0.05});
        const orbitLine = new THREE.Line(orbitPoints, orbitMaterial);
        orbitLine.computeLineDistances(); // Necesario para que funcione la línea punteada
        scene.add(orbitLine);

        // Crear el satélite
        const satelliteGeometry = new THREE.SphereGeometry(satelliteSize, 16, 16);
        const satelliteMaterial = new THREE.MeshBasicMaterial({color: 0xFFFFFF});
        const satelliteMesh = new THREE.Mesh(satelliteGeometry, satelliteMaterial);

        // Inicializar posición del satélite
        satelliteMesh.userData = {
          orbitRadius: orbitRadius,
          angle: (index / this.satellites.length) * (2 * Math.PI), // Ángulo inicial diferenciado por satélite
          speed: 0.005 + Math.random() * 0.002, // Velocidad de rotación variable
          inclination: THREE.MathUtils.degToRad(satellite.inclination)
        };

        scene.add(satelliteMesh);
        this.satelliteObjects.push(satelliteMesh); // Guardar para la animación
      });
    },

    animateSatellites() {
      this.satelliteObjects.forEach((satellite) => {
        // Actualizar ángulo del satélite en función de su velocidad
        satellite.userData.angle += satellite.userData.speed;

        // Usar trigonometría para actualizar la posición del satélite en la órbita
        const x = Math.cos(satellite.userData.angle) * satellite.userData.orbitRadius;
        const y = Math.sin(satellite.userData.angle) * satellite.userData.orbitRadius * Math.cos(satellite.userData.inclination);
        const z = Math.sin(satellite.userData.angle) * satellite.userData.orbitRadius * Math.sin(satellite.userData.inclination);

        satellite.position.set(x, y, z);
      });
    },

    toggleRotation() {
      this.isRotating = !this.isRotating;
    },

    showSatelliteInfo2(satellite) {
      this.selectedSatellite = satellite;
    },

    closeModal() {
      this.selectedSatellite = null; // Cerrar la ventana modal
    }
  }
};
</script>

<style>
body {
  background-color: #121212;
  color: #ffffff;
  margin: 0;
  font-family: 'Arial', sans-serif;
}

.header {
  text-align: center;
  padding: 20px;
  background-color: #1a1a1a;
}

h1 {
  margin: 0;
}

.toggle-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.main-content {
  display: flex;
  justify-content: space-between;
}

.sidebar {
  width: 25%;
  background-color: #1c1c1c;
  padding: 20px;
  border-radius: 5px;
}

.interaction-area {
  width: 75%;
  position: relative;
}

.canvas-container {
  width: 100%;
  height: 600px;
  position: relative;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: #2c2c2c;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  color: #ffffff;
}

.canvas-container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}


html, body {
  height: 100%; /* Asegurar que el body ocupe toda la altura de la ventana */
  margin: 0; /* Sin margen por defecto */
  overflow: hidden; /* Evitar el scroll en el body */
  background-color: #121212; /* Fondo oscuro para el body */
  color: #ffffff; /* Texto en color blanco */
}

.container {
  display: flex; /* Usar flexbox para disposición */
  height: 100%; /* Altura completa */
}

.sidebar {
  background-color: #1e1e1e; /* Color de fondo oscuro para el aside */
  padding: 20px; /* Espaciado interno */
  width: 300px; /* Ancho de la barra lateral */
  height: 100vh; /* Altura completa de la ventana */
  overflow-y: auto; /* Habilitar desplazamiento vertical */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3); /* Sombra para dar profundidad */
  border-right: 1px solid #333; /* Línea de separación a la derecha */
}

.content {
  flex-grow: 1; /* El contenido principal ocupará el espacio restante */
  padding: 20px; /* Espaciado interno */
  overflow: auto; /* Permitir desplazamiento si es necesario */
  background-color: #121212; /* Fondo oscuro para el contenido */
  color: #ffffff; /* Texto en color blanco */
}
html,
body {
  height: 100%; /* Asegurar que el body ocupe toda la altura de la ventana */
  margin: 0; /* Sin margen por defecto */
  overflow: hidden; /* Evitar el scroll en el body */
  background-color: #121212; /* Fondo oscuro para el body */
  color: #ffffff; /* Texto en color blanco */
}

.container {
  display: flex; /* Usar flexbox para disposición */
  height: 100%; /* Altura completa */
}

.sidebar {
  background-color: #1e1e1e; /* Color de fondo oscuro para el aside */
  padding: 20px; /* Espaciado interno */
  width: 300px; /* Ancho de la barra lateral */
  height: 100vh; /* Altura completa de la ventana */
  overflow-y: auto; /* Habilitar desplazamiento vertical */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3); /* Sombra para dar profundidad */
  border-right: 1px solid #333; /* Línea de separación a la derecha */
}

.content {
  flex-grow: 1; /* El contenido principal ocupará el espacio restante */
  padding: 20px; /* Espaciado interno */
  overflow: auto; /* Permitir desplazamiento si es necesario */
  background-color: #121212; /* Fondo oscuro para el contenido */
  color: #ffffff; /* Texto en color blanco */
}

h2,
h3 {
  color: #e0e0e0; /* Color claro para los encabezados */
}

p,
ul {
  font-size: 1em; /* Tamaño de texto normal */
  color: #cccccc; /* Color del texto en gris claro */
  line-height: 1.5; /* Altura de línea para mejor legibilidad */
}

ul {
  list-style-type: none; /* Sin viñetas */
  padding-left: 0; /* Sin margen a la izquierda */
}

li {
  margin-bottom: 5px; /* Espacio entre los elementos de la lista */
  cursor: pointer; /* Cambia el cursor al pasar el mouse */
  transition: color 0.3s; /* Transición suave para el color */
}

li:hover {
  color: #ffffff; /* Cambiar color al pasar el mouse */
}

.carousel {
  position: relative;
  margin-top: 20px; /* Espacio superior */
}

.carousel-images {
  display: flex;
  transition: transform 0.5s ease; /* Transición suave al cambiar de imagen */
  width: 100%; /* Ancho completo */
  height: 200px; /* Altura fija */
}

.carousel-images img {
  min-width: 100%; /* Cada imagen ocupa el 100% del contenedor */
  height: 100%; /* Ajustar la altura de la imagen */
  object-fit: cover; /* Mantener la proporción de la imagen */
}

.carousel-button {
  position: absolute;
  top: 50%; /* Centrar verticalmente */
  transform: translateY(-50%); /* Ajustar el posicionamiento */
  background-color: rgba(255, 255, 255, 0.1); /* Fondo semitransparente oscuro */
  color: #ffffff; /* Color del texto en blanco */
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px; /* Bordes redondeados para los botones */
}

.carousel-button:first-of-type {
  left: 10px; /* Botón de anterior */
}

.carousel-button:last-of-type {
  right: 10px; /* Botón de siguiente */
}

/* Estilo del scrollbar */
.sidebar::-webkit-scrollbar {
  width: 8px; /* Ancho de la barra de desplazamiento */
}

.sidebar::-webkit-scrollbar-track {
  background: #2c2c2c; /* Fondo de la pista */
}

.sidebar::-webkit-scrollbar-thumb {
  background: #555; /* Color del pulgar de la barra de desplazamiento */
  border-radius: 10px; /* Bordes redondeados para el pulgar */
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #777; /* Color del pulgar al pasar el mouse */
}
</style>
