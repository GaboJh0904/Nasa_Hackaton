<template>
  <div id="app">
    <h1>Detección de Manos con Vue.js</h1>
    <div ref="solarSystemContainer" class="solar-system"></div>
    <HandDetector />
  </div>
</template>

<script>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import HandDetector from './components/HandDetector.vue';

export default {
  name: 'SolarSystem',
  mounted() {
    this.initSolarSystem();
  },
  components: {
    HandDetector,
  },
  methods: {
    initSolarSystem() {
      // Configuración básica
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(window.innerWidth, window.innerHeight);
      this.$refs.solarSystemContainer.appendChild(renderer.domElement);

      // Añadir luz
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      const pointLight = new THREE.PointLight(0xffffff, 1, 0);
      pointLight.position.set(0, 0, 0); // El Sol
      scene.add(pointLight);

      // Crear el Sol
      const sunGeometry = new THREE.SphereGeometry(5, 32, 32);
      const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffd700 });
      const sun = new THREE.Mesh(sunGeometry, sunMaterial);
      scene.add(sun);

      // Añadir planetas
      const planets = [];
      const planetData = [
        { size: 0.5, distance: 10, color: 0xaaaaaa }, // Mercurio
        { size: 1, distance: 15, color: 0xffd700 },  // Venus
        { size: 1.2, distance: 20, color: 0x0000ff }, // Tierra
        { size: 0.7, distance: 25, color: 0xff4500 }  // Marte
        // Agregar más planetas si lo deseas
      ];

      planetData.forEach(data => {
        const geometry = new THREE.SphereGeometry(data.size, 32, 32);
        const material = new THREE.MeshStandardMaterial({ color: data.color });
        const planet = new THREE.Mesh(geometry, material);

        planet.position.x = data.distance;
        planets.push(planet);
        scene.add(planet);
      });

      // Controles orbitales para interactividad
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.25;
      controls.enableZoom = true;

      camera.position.z = 50;

      // Animación
      const animate = () => {
        requestAnimationFrame(animate);

        // Rotación del Sol
        sun.rotation.y += 0.005;

        // Rotar los planetas alrededor del Sol
        planets.forEach((planet, index) => {
          planet.position.x = Math.cos(Date.now() * 0.001 * (index + 1)) * planetData[index].distance;
          planet.position.z = Math.sin(Date.now() * 0.001 * (index + 1)) * planetData[index].distance;
          planet.rotation.y += 0.01;
        });

        controls.update();
        renderer.render(scene, camera);
      };

      animate();

      // Ajustar el tamaño del renderizado al redimensionar la ventana
      window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      });
    },
  },
};
</script>

<style>
.solar-system {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
#app {
  position: relative;
}
h1 {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1;
  color: white;
}
</style>
