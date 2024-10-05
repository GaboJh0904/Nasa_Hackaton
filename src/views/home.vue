<template>
    <div id="home">
      <div ref="canvasContainer" class="canvas-container"></div>
      <div v-if="selectedPlanet" class="info-panel">
        <h2>{{ selectedPlanet.name }}</h2>
        <p>{{ selectedPlanet.description }}</p>
        <button @click="navigateToPlanet">Ir a {{ selectedPlanet.name }}</button>
        <button @click="closeInfo">Cerrar</button>
      </div>
    </div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { useRouter } from 'vue-router'; // Usar useRouter para la navegación
  import backgroundTexture from '@/assets/space-background.jpg';
  import marsTexture from '@/assets/mars.jpg';
  
  export default {
    setup() {
      const canvasContainer = ref(null);
      const selectedPlanet = ref(null);
      const router = useRouter(); // Obtén el router para navegar entre rutas
      let scene, camera, renderer, controls, planets = [];
      let orbitGroup;
  
      const initScene = () => {
        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        canvasContainer.value.appendChild(renderer.domElement);
  
        controls = new OrbitControls(camera, renderer.domElement);
        scene.background = new THREE.TextureLoader().load(backgroundTexture);
  
        camera.position.z = 30;
  
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(10, 10, 10).normalize();
        scene.add(light);
  
        orbitGroup = new THREE.Group();
        scene.add(orbitGroup);
  
        window.addEventListener('resize', onWindowResize);
        renderer.domElement.addEventListener('click', onCanvasClick);
      };
  
      const onWindowResize = () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        controls.update();
      };
  
      const addPlanets = () => {
        const planetData = [
          { name: 'Mercurio', radius: 0.5, distance: 3, description: 'El planeta más cercano al Sol.' },
          { name: 'Venus', radius: 0.6, distance: 5, description: 'Conocido como el planeta hermano de la Tierra.' },
          { name: 'Tierra', radius: 0.6, distance: 7, description: 'Nuestro hogar.', route: '/planets/earth' },
          { name: 'Marte', radius: 0.5, distance: 9, description: 'El planeta rojo.' },
          { name: 'Júpiter', radius: 1.2, distance: 12, description: 'El planeta más grande del sistema solar.' },
          { name: 'Saturno', radius: 1.1, distance: 15, description: 'Famoso por sus anillos.' },
          { name: 'Urano', radius: 1.0, distance: 18, description: 'Un gigante de gas.' },
          { name: 'Neptuno', radius: 0.9, distance: 21, description: 'El planeta más alejado del Sol.' },
        ];
  
        planetData.forEach(data => {
          const geometry = new THREE.SphereGeometry(data.radius, 32, 32);
          const textureLoader = new THREE.TextureLoader();
          const material = new THREE.MeshBasicMaterial({ map: textureLoader.load(marsTexture) });
          const planet = new THREE.Mesh(geometry, material);
  
          planet.position.x = data.distance;
          planet.userData = data;
          orbitGroup.add(planet);
          planets.push(planet);
        });
      };
  
      const onCanvasClick = (event) => {
        const mouse = new THREE.Vector2();
        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  
        const raycaster = new THREE.Raycaster();
        raycaster.setFromCamera(mouse, camera);
  
        const intersects = raycaster.intersectObjects(planets);
  
        if (intersects.length > 0) {
          selectedPlanet.value = intersects[0].object.userData;
        }
      };
  
      const closeInfo = () => {
        selectedPlanet.value = null;
      };
  
      const navigateToPlanet = () => {
        if (selectedPlanet.value.route) {
          router.push(selectedPlanet.value.route); // Navegar a la ruta del planeta seleccionado
        }
      };
  
      const animate = () => {
        requestAnimationFrame(animate);
        planets.forEach(planet => {
          planet.rotation.y += 0.01;
        });
        orbitGroup.rotation.y += 0.001;
        controls.update();
        renderer.render(scene, camera);
      };
  
      onMounted(() => {
        initScene();
        addPlanets();
        animate();
      });
  
      onBeforeUnmount(() => {
        window.removeEventListener('resize', onWindowResize);
        renderer.domElement.removeEventListener('click', onCanvasClick);
      });
  
      return {
        canvasContainer,
        selectedPlanet,
        closeInfo,
        navigateToPlanet,
      };
    }
  };
  </script>
  
  <style>
#app {
  position: relative;
  overflow: hidden;
}

.canvas-container {
  width: 100%;
  height: 100vh;
}

.info-panel {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border: 1px solid #ccc;
  z-index: 10;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.info-panel h2 {
  margin: 0;
}

.info-panel button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.info-panel button:hover {
  background-color: #0056b3;
}
</style>
