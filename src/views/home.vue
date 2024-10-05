<template>
  <div id="home">
    <div ref="canvasContainer" class="canvas-container"></div>
    <div v-if="selectedPlanet" class="info-panel">
      <h2>{{ selectedPlanet.name }}</h2>
      <p>{{ selectedPlanet.description }}</p>
      <button @click="resetView">Alejar</button>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { ref, onMounted, onBeforeUnmount } from 'vue';

// Importar las texturas de los planetas
import mercurioTexture from '@/assets/mercurio.jpg';
import venusTexture from '@/assets/mars.jpg';
import tierraTexture from '@/assets/earth.jpg';
import marsTexture from '@/assets/mars.jpg';
import jupiterTexture from '@/assets/jupiter.jpg';
import saturnoTexture from '@/assets/saturno.jpg';
import uranoTexture from '@/assets/mars.jpg';
import neptunoTexture from '@/assets/mars.jpg';
import marteTexture from "@/assets/mars.jpg";

export default {
  setup() {
    const canvasContainer = ref(null);
    const selectedPlanet = ref(null);
    let scene, camera, renderer, controls, planets = [];
    let orbitGroup;
    let targetPlanet = null; // Para almacenar el planeta objetivo
    let isRotating = true; // Estado de rotación del sistema solar
    let zoomIn = true; // Para manejar el estado de acercamiento

    const initScene = () => {
      // Crear escena y cámara
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      renderer.setSize(window.innerWidth, window.innerHeight);
      canvasContainer.value.appendChild(renderer.domElement);

      // Añadir controles de órbita
      controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true; // Suavizar el movimiento
      controls.dampingFactor = 0.25;
      controls.screenSpacePanning = false;

      // Fondo negro para simular el espacio
      scene.background = new THREE.Color(0x000000);

      // Posicionar la cámara
      camera.position.z = 70;

      // Añadir luz
      const light = new THREE.DirectionalLight(0xffffff, 1);
      light.position.set(10, 10, 10).normalize();
      scene.add(light);

      // Crear el Sol
      const sunGeometry = new THREE.SphereGeometry(3, 32, 32);
      const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffdd00 });
      const sun = new THREE.Mesh(sunGeometry, sunMaterial);
      scene.add(sun);

      // Añadir luz del Sol
      const sunLight = new THREE.PointLight(0xffdd00, 2, 100);
      sunLight.position.set(0, 0, 0);
      scene.add(sunLight);

      // Crear un resplandor para el Sol
      const glowGeometry = new THREE.SphereGeometry(3.5, 32, 32);
      const glowMaterial = new THREE.MeshBasicMaterial({
        color: 0xffdd00,
        transparent: true,
        opacity: 0.6,
      });
      const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
      scene.add(glowMesh);

      // Añadir un grupo para la órbita de los planetas
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
        { name: 'Mercurio', radius: 0.3, distance: 10, rotationSpeed: 0.01, texture: mercurioTexture, description: 'El planeta más cercano al Sol.' },
        { name: 'Venus', radius: 0.4, distance: 15, rotationSpeed: 0.005, texture: venusTexture, description: 'Conocido como el planeta hermano de la Tierra.' },
        { name: 'Tierra', radius: 0.5, distance: 20, rotationSpeed: 0.02, texture: tierraTexture, description: 'Nuestro hogar.' },
        { name: 'Marte', radius: 0.4, distance: 25, rotationSpeed: 0.015, texture: marteTexture, description: 'El planeta rojo.' },
        { name: 'Júpiter', radius: 0.8, distance: 32, rotationSpeed: 0.02, texture: jupiterTexture, description: 'El planeta más grande del sistema solar.' },
        { name: 'Saturno', radius: 0.7, distance: 40, rotationSpeed: 0.008, texture: saturnoTexture, description: 'Famoso por sus anillos.' },
        { name: 'Urano', radius: 0.6, distance: 50, rotationSpeed: 0.007, texture: uranoTexture, description: 'Un gigante de gas.' },
        { name: 'Neptuno', radius: 0.5, distance: 60, rotationSpeed: 0.006, texture: neptunoTexture, description: 'El planeta más alejado del Sol.' },
      ];

      planetData.forEach(data => {
        const geometry = new THREE.SphereGeometry(data.radius, 32, 32);
        const textureLoader = new THREE.TextureLoader();
        const material = new THREE.MeshBasicMaterial({map: textureLoader.load(data.texture)}); // Usar la textura correspondiente
        const planet = new THREE.Mesh(geometry, material);

        // Posicionar el planeta en su órbita
        planet.position.x = data.distance;
        planet.rotationSpeed = data.rotationSpeed; // Guardar velocidad de rotación
        planet.userData = data; // Guardar información del planeta
        orbitGroup.add(planet); // Agregar el planeta al grupo de órbita
        planets.push(planet);

        // Agregar anillos a Saturno
        if (data.name === 'Saturno') {
          const ringGeometry = new THREE.RingGeometry(1.1, 1.8, 32);
          const ringMaterial = new THREE.MeshBasicMaterial({
            map: textureLoader.load(marsTexture), // Puedes usar otra textura para los anillos
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.5
          });
          const ring = new THREE.Mesh(ringGeometry, ringMaterial);
          ring.rotation.x = - Math.PI / 2; // Rotar los anillos para que estén planos
          planet.add(ring); // Añadir el anillo al planeta
        }
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
        selectedPlanet.value = intersects[0].object.userData; // Obtener datos del planeta seleccionado
        targetPlanet = intersects[0].object; // Establecer el planeta objetivo para acercar
        isRotating = false; // Detener la rotación del sistema solar
        zoomIn = true; // Activar la transición de acercamiento
      }
    };

    const moveToPlanet = () => {
      if (targetPlanet) {
        const targetPosition = new THREE.Vector3();
        targetPlanet.getWorldPosition(targetPosition); // Obtener la posición global del planeta

        // Mover la cámara hacia el planeta
        const distanceToPlanet = targetPosition.distanceTo(camera.position);
        const zoomSpeed = 0.05; // Velocidad de acercamiento

        if (distanceToPlanet > 5) { // Continuar acercándose hasta llegar cerca del planeta
          camera.position.lerp(targetPosition.clone().add(new THREE.Vector3(0, 0, 5)), zoomSpeed); // Acercar a 5 unidades del planeta
          controls.target.copy(targetPosition); // Centrar controles en el planeta
          controls.update();
        } else {
          // Después de acercarse, habilitar la rotación de la vista 360 grados
          controls.enableZoom = true; // Habilitar zoom para la vista de 360 grados
          zoomIn = true; // Desactivar zoom en este estado
        }
      }
    };

    const resetView = () => {
      selectedPlanet.value = null; // Cerrar panel de información
      targetPlanet = null; // Restablecer el planeta objetivo
      isRotating = true; // Reiniciar la rotación
      camera.position.z = 70; // Regresar a la posición inicial
      controls.target.set(0, 0, 0); // Restablecer el objetivo de los controles
      controls.update();
      controls.enableZoom = true ; // Deshabilitar zoom
    };

    const animate = () => {
      requestAnimationFrame(animate);

      if (isRotating) {
        orbitGroup.rotation.y += 0.005; // Rotar el sistema solar
      }

      if (zoomIn) {
        moveToPlanet(); // Manejar el movimiento de acercamiento al planeta
      }

      controls.update(); // Actualizar controles
      renderer.render(scene, camera); // Renderizar la escena
    };

    onMounted(() => {
      initScene();
      addPlanets();
      animate();
    });

    onBeforeUnmount(() => {
      window.removeEventListener('resize', onWindowResize);
      renderer.dispose(); // Limpiar recursos
    });

    return { canvasContainer, selectedPlanet, resetView };
  },
};
</script>

<style>
.canvas-container {
  width: 100vw;
  height: 100vh;
  position: relative;
}

.info-panel {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(255, 255, 255, 0.8);
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

button {
  background-color: #007bff;
  border: none;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
