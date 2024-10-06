<template>
  <div id="app">
    <header class="header">
      <h1>Planeta Tierra y Satélites con Áreas de Calor</h1>
      <button class="toggle-button" @click="toggleRotation">{{ isRotating ? 'Detener Rotación' : 'Reanudar Rotación' }}</button>
      <HandDetector/>
    </header>

    <div class="main-content">
      <aside class="sidebar">
        <h2>Información del Planeta</h2>
        <p><strong>Nombre:</strong> Tierra</p>
        <p><strong>Radio:</strong> 6,371 km</p>
        <p><strong>Masa:</strong> 5.972 × 10<sup>24</sup> kg</p>
        <p><strong>Temperatura Promedio:</strong> 15 °C</p>
        <p><strong>Satélites Naturales:</strong> 1 (Luna)</p>
        <h3>Satélites Artificiales</h3>
        <ul>
          <li v-for="(satellite, index) in satellites" :key="index" @click="showSatelliteInfo(satellite)">
            Satélite {{ index + 1 }} - Radio Órbita: {{ satellite.orbitRadius.toFixed(2) }} km
          </li>
        </ul>
      </aside>

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
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import earthTexture from "@/assets/tierra.png"; // Textura del planeta Tierra
import HandDetector from "@/components/HandDetector.vue";

export default {
  components: {
    HandDetector,
  },
  name: "App",
  data() {
    return {
      isRotating: true,
      satellites: [
        { name: 'Hubble', orbitRadius: 2, purpose: 'Observación del espacio' },
        { name: 'ISS', orbitRadius: 2.5, purpose: 'Investigación científica' },
        { name: 'GOES', orbitRadius: 3, purpose: 'Monitoreo climático' }
      ],
      heatMapTexture: null, // Textura de las áreas de calor
      heatSpots: [], // Zonas de calor
      selectedSatellite: null // Satélite seleccionado para mostrar información
    };
  },
  mounted() {
    this.createEarth();
  },
  methods: {
    createEarth() {
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      camera.position.z = 3;

      const renderer = new THREE.WebGLRenderer({ alpha: true });
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
          this.animateSatellites(); // Animar los satélites
          this.updateHeatMapTexture(); // Actualizar textura de las áreas calientes
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
        { lat: -3.4653, lon: -62.2159, radius: 30, intensity: 0.6 }, // Amazonas
        { lat: -25.2744, lon: 133.7751, radius: 25, intensity: 0.8 }, // Australia
        { lat: 1.2921, lon: 36.8219, radius: 20, intensity: 0.4 }, // África central
        { lat: 40.4637, lon: -3.7492, radius: 20, intensity: 0.5 }, // España
        { lat: -11.2027, lon: 17.8739, radius: 15, intensity: 0.7 }, // Angola
      ];
    },

    updateHeatMapTexture() {
      const ctx = this.heatMapTexture.image.getContext("2d");

      // Limpiar el lienzo
      ctx.clearRect(0, 0, 512, 512);

      // Dibujar las áreas calientes (simulando llamas)
      this.heatSpots.forEach((spot) => {
        const { x, y } = this.convertLatLonToCanvasCoords(spot.lat, spot.lon);

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
      return { x, y };
    },

    createSatellites(scene) {
      const satelliteCount = this.satellites.length; // Usar el número de satélites definido en data
      const orbitRadius = 1.5; // Radio de la órbita alrededor de la Tierra
      const satelliteSize = 0.05; // Tamaño de los satélites

      for (let i = 0; i < satelliteCount; i++) {
        // Crear la órbita
        const orbitGeometry = new THREE.CircleGeometry(orbitRadius, 64);
        const orbitMaterial = new THREE.LineDashedMaterial({ color: 0x888888 });
        const orbit = new THREE.Line(orbitGeometry, orbitMaterial);
        orbit.rotation.x = Math.PI / 2; // Alinear la órbita horizontalmente
        scene.add(orbit);

        // Crear el satélite
        const satelliteGeometry = new THREE.SphereGeometry(satelliteSize, 16, 16);
        const satelliteMaterial = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
        const satellite = new THREE.Mesh(satelliteGeometry, satelliteMaterial);

        // Posicionar el satélite en la órbita
        const angle = (i / satelliteCount) * (2 * Math.PI); // Espaciar satélites en la órbita
        satellite.position.set(orbitRadius * Math.cos(angle), orbitRadius * Math.sin(angle), 0);
        scene.add(satellite);
        satellite.userData = this.satellites[i]; // Guardar información del satélite en su userdata

        satellite.rotation.z = Math.random() * Math.PI; // Rotación aleatoria del satélite
      }
    },

    animateSatellites() {
      const satellites = this.$refs.canvasContainer.children;
      const satelliteCount = satellites.length;

      for (let i = 0; i < satelliteCount; i++) {
        const satellite = satellites[i];
        if (satellite.userData) {
          const angle = Date.now() * 0.001 + (i / satelliteCount) * (2 * Math.PI); // Movimiento orbital
          satellite.position.x = Math.cos(angle) * 1.5; // Radio de la órbita
          satellite.position.y = Math.sin(angle) * 1.5;
        }
      }
    },

    toggleRotation() {
      this.isRotating = !this.isRotating;
    },

    showSatelliteInfo(satellite) {
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

</style>
