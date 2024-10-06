<template>
  <div id="home">
    <!-- Barra superior -->
    <div class="top-bar">
      <!-- Botón de navegación -->
      <button class="nav-button" @click="goBack">⬅ Atrás</button>
      <!-- Título central -->
      <h1>Sistema Solar</h1>
      <!-- Botón para detener/reanudar el movimiento de los planetas -->
      <button class="pause-button" @click="toggleRotation">
        {{ isRotating ? 'Detener' : 'Reanudar' }} Movimiento
      </button>
    </div>
    <!-- Cuadro emergente -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>¡Bienvenido al Sistema de Exploración Espacial Avanzada!</h2>
        <p>
          Nos complace darte la bienvenida a esta plataforma interactiva,
          diseñada especialmente para aquellos que buscan profundizar en los
          misterios del cosmos. Este sistema avanzado no solo te permitirá
          explorar el sistema solar, sino que también te brindará acceso a
          información detallada, simulaciones y visualizaciones en 3D para
          comprender las complejidades de los planetas, asteroides y otros
          cuerpos celestes.
        </p>
        <p>
          Como estudiante universitario, tendrás la oportunidad de sumergirte en
          un entorno de aprendizaje inmersivo, donde la precisión científica y
          la tecnología de última generación convergen para ofrecerte una
          experiencia educativa única. Aprovecha este recurso para explorar más
          allá de los conceptos básicos y obtener un conocimiento avanzado que
          enriquecerá tus estudios y proyectos de investigación.
        </p>
        <button @click="closeModal">Comenzar la Exploración</button>
      </div>
    </div>

    <!-- Contenido de la página -->
    <div ref="canvasContainer" class="canvas-container"></div>
    <div v-if="selectedPlanet" class="info-panel">
      <h2>{{ selectedPlanet.name }}</h2>
      <p>{{ selectedPlanet.description }}</p>
      <!-- Mostrar el botón solo si no es un cometa o asteroide -->
      <button
        v-if="
          selectedPlanet.name !== 'Cometa' &&
          selectedPlanet.name !== 'Asteroide'
        "
        @click="navigateToPlanet"
      >
        Ir a {{ selectedPlanet.name }}
      </button>
      <!-- Botón de alejamiento -->
      <button @click="resetView">Alejar</button>
    </div>
  </div>
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router"; // Importar el router

// Importar las texturas de los planetas
import mercurioTexture from "@/assets/mercurio.jpg";
import venusTexture from "@/assets/venus.jpeg";
import tierraTexture from "@/assets/earth.jpg";
import marsTexture from "@/assets/mars.jpg";
import jupiterTexture from "@/assets/jupiter.jpg";
import saturnoTexture from "@/assets/saturno.jpg";
import uranoTexture from "@/assets/urano.jpeg";
import neptunoTexture from "@/assets/neptuno.jpg";
import marteTexture from "@/assets/mars.jpg";
import anillos from "@/assets/anillo.jpg";
import starsTexture from "@/assets/textura_estrella.jpg";
import solTexture from "@/assets/textura_sol.jpg";

export default {
  setup() {
    const showModal = ref(true); // Estado para mostrar el modal
    const closeModal = () => {
      showModal.value = false; // Ocultar el modal cuando se presione el botón
    };
    const canvasContainer = ref(null);
    const selectedPlanet = ref(null);
    const router = useRouter(); // Obtener el enrutador para manejar la navegación
    let scene,
      camera,
      renderer,
      controls,
      planets = [];
    let orbitGroup;
    let targetPlanet = null; // Para almacenar el planeta objetivo
    const isRotating = ref(true); // Controla si los planetas están rotando o no
    let zoomIn = true; // Para manejar el estado de acercamiento
    let sun; // Variable para el Sol

    // Función para regresar a la página anterior
    const goBack = () => {
      router.back();
    };

    // Función para alternar la rotación de los planetas
    const toggleRotation = () => {
      isRotating.value = !isRotating.value;
    };

    const addComets = () => {
      const textureLoader = new THREE.TextureLoader();
      const material = new THREE.MeshBasicMaterial({
        map: textureLoader.load(marsTexture), // Textura de Marte temporal
      });

      // Generar 10 cometas con tamaños más grandes
      for (let i = 0; i < 10; i++) {
        const radius = Math.random() * 1 + 0.5; // Tamaño aleatorio entre 0.5 y 1.5 (cometas más grandes)
        const geometry = new THREE.SphereGeometry(radius, 16, 16); // Esferas más grandes para cometas

        const comet = new THREE.Mesh(geometry, material);
        comet.userData = {
          name: "Cometa",
          description: "Un cometa viajando a través del sistema solar.",
        };

        // Posición más cercana para hacer visibles los cometas
        const posX = (Math.random() - 0.5) * 100; // Rango de -50 a 50
        const posY = (Math.random() - 0.5) * 100; // Rango de -50 a 50
        const posZ = (Math.random() - 0.5) * 100; // Rango de -50 a 50

        comet.position.set(posX, posY, posZ);
        scene.add(comet);
        planets.push(comet); // Añadirlo a la lista de planetas para interactuar con raycaster
      }
    };

    const addAsteroids = () => {
      const textureLoader = new THREE.TextureLoader();
      const material = new THREE.MeshBasicMaterial({
        map: textureLoader.load(marsTexture), // Textura de Marte temporal
      });

      // Generar 15 asteroides con tamaños más grandes
      for (let i = 0; i < 15; i++) {
        const radius = Math.random() * 1.5 + 0.5; // Tamaño aleatorio entre 0.5 y 2 (asteroides más grandes)
        const geometry = new THREE.SphereGeometry(radius, 16, 16); // Esferas más grandes para asteroides

        const asteroid = new THREE.Mesh(geometry, material);
        asteroid.userData = {
          name: "Asteroide",
          description: "Un asteroide moviéndose en el sistema solar.",
        };

        // Posición más cercana para hacer visibles los asteroides
        const posX = (Math.random() - 0.5) * 150; // Rango de -75 a 75
        const posY = (Math.random() - 0.5) * 150; // Rango de -75 a 75
        const posZ = (Math.random() - 0.5) * 150; // Rango de -75 a 75

        asteroid.position.set(posX, posY, posZ);
        scene.add(asteroid);
        planets.push(asteroid); // Añadirlo a la lista de planetas para interactuar con raycaster
      }
    };

    const addStars = () => {
      const textureLoader = new THREE.TextureLoader();
      const material = new THREE.MeshBasicMaterial({
        map: textureLoader.load(starsTexture),
      }); // Usaremos temporalmente la textura de Marte

      // Generar 100 estrellas
      for (let i = 0; i < 200; i++) {
        const radius = Math.random() * 0.4 + 0.2; // Tamaño pequeño para las estrellas, entre 0.02 y 0.12
        const geometry = new THREE.SphereGeometry(radius, 16, 16);

        const star = new THREE.Mesh(geometry, material);

        // Posición aleatoria, pero con mayor distancia (más allá del último planeta)
        const distance = Math.random() * 600 + 300; // Distancia aleatoria entre 150 y 550 (más allá de Neptuno)

        // Aleatorizar posiciones en un espacio tridimensional alrededor del sistema solar
        const posX = (Math.random() - 0.5) * distance * 2; // Distribuir en un rango más amplio
        const posY = (Math.random() - 0.5) * distance * 2;
        const posZ = (Math.random() - 0.5) * distance * 2;

        star.position.set(posX, posY, posZ);

        // Añadir la estrella a la escena
        scene.add(star);
      }
    };

    const initScene = () => {
      // Crear escena y cámara
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
      );
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
      sun = new THREE.Mesh(sunGeometry, sunMaterial);
      sun.userData = {
        name: "Sol",
        texture: solTexture,
        description:
          "El Sol es la estrella en el centro del Sistema Solar. Genera energía a través de la fusión nuclear y es el principal proveedor de luz y calor para la vida en la Tierra.",
      };

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
      orbitGroup.add(sun); // Añadir el Sol al grupo de órbita
      planets.push(sun); // Añadir el Sol a la lista de planetas
      scene.add(orbitGroup);

      window.addEventListener("resize", onWindowResize);
      renderer.domElement.addEventListener("click", onCanvasClick);

      // Llamada a las funciones para añadir cometas y asteroides
      //addComets();
      //addAsteroids();

      // Añadir estrellas
      addStars();
    };

    const onWindowResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      controls.update();
    };

    const addPlanets = () => {
      const planetData = [
        {
          name: "Mercurio",
          radius: 0.3,
          distance: 8,
          rotationSpeed: 0.04,
          texture: mercurioTexture,
          orbitInclination: 7,
          orbitDirection: 1,
          description:
            "Mercurio es el planeta más cercano al Sol. Es un cuerpo rocoso similar a la Luna, con una superficie llena de cráteres y temperaturas extremas. Dado su tamaño y cercanía al Sol, Mercurio tiene una atmósfera muy delgada. Este planeta es un excelente objeto de estudio para entender la formación de cuerpos terrestres en el sistema solar.",
        },
        {
          name: "Venus",
          radius: 0.5,
          distance: 11,
          rotationSpeed: 0.015,
          texture: venusTexture,
          orbitInclination: 3.4,
          orbitDirection: -1,
          description:
            'Venus es el segundo planeta desde el Sol y a menudo es llamado el "planeta hermano" de la Tierra debido a su tamaño y composición similares. Sin embargo, Venus tiene una atmósfera densa y tóxica que atrapa el calor, convirtiéndolo en el planeta más caliente del sistema solar, con temperaturas superiores a los 460°C. Es un laboratorio natural para estudiar los efectos del efecto invernadero.',
        },
        {
          name: "Tierra",
          radius: 0.6,
          distance: 15,
          rotationSpeed: 0.01,
          texture: tierraTexture,
          orbitInclination: 0,
          orbitDirection: 1,
          description:
            "La Tierra es el único planeta conocido que alberga vida. Está cubierta por océanos que ocupan más del 70% de su superficie y tiene una atmósfera rica en oxígeno. La presencia de una magnetosfera y una atmósfera moderada permite un entorno adecuado para la vida tal como la conocemos. Es el tercer planeta desde el Sol.",
        },
        {
          name: "Marte",
          radius: 0.4,
          distance: 22,
          rotationSpeed: 0.008,
          texture: marteTexture,
          orbitInclination: 1.85,
          orbitDirection: 1,
          description:
            'Marte, conocido como el "planeta rojo", es el cuarto planeta desde el Sol. Su color característico proviene del óxido de hierro en su superficie. Marte tiene la montaña más alta del sistema solar, el Monte Olimpo, y alberga valles y sistemas fluviales que sugieren que alguna vez tuvo agua líquida. Estudiar Marte es clave para entender la habitabilidad en otros planetas.',
        },
        {
          name: "Júpiter",
          radius: 1.0,
          distance: 35,
          rotationSpeed: 0.005,
          texture: jupiterTexture,
          orbitInclination: 1.3,
          orbitDirection: -1,
          description:
            "Júpiter es el planeta más grande del sistema solar, con una masa que es más de dos veces la de todos los demás planetas combinados. Está compuesto principalmente de hidrógeno y helio. Su característica más distintiva es la Gran Mancha Roja, una tormenta que ha estado activa durante cientos de años. Júpiter tiene más de 75 lunas, incluido el volcán más activo del sistema solar en su luna Ío.",
        },
        {
          name: "Saturno",
          radius: 0.9,
          distance: 50,
          rotationSpeed: 0.003,
          texture: saturnoTexture,
          orbitInclination: 2.48,
          orbitDirection: 1,
          description:
            "Saturno es famoso por su sistema de anillos, que están compuestos de partículas de hielo y roca. Aunque todos los planetas gigantes tienen anillos, los de Saturno son los más extensos y visibles desde la Tierra. Este gigante gaseoso también tiene más de 80 lunas, incluyendo Titán, la segunda luna más grande del sistema solar, que tiene una atmósfera densa y lagos de metano.",
        },
        {
          name: "Urano",
          radius: 0.7,
          distance: 65,
          rotationSpeed: 0.002,
          texture: uranoTexture,
          orbitInclination: 0.77,
          orbitDirection: -1,
          description:
            "Urano es único en el sistema solar porque gira de lado, lo que significa que su eje de rotación está casi alineado con su plano orbital. Es un gigante helado compuesto de agua, amoníaco y metano sobre un pequeño núcleo rocoso. Su atmósfera rica en metano le da su color azul verdoso.",
        },
        {
          name: "Neptuno",
          radius: 0.6,
          distance: 80,
          rotationSpeed: 0.0018,
          texture: neptunoTexture,
          orbitInclination: 1.77,
          orbitDirection: 1,
          description:
            "Neptuno es el planeta más alejado del Sol y el cuarto gigante gaseoso del sistema solar. Tiene vientos extremadamente rápidos y tormentas masivas, incluida la Gran Mancha Oscura, una tormenta similar a la Gran Mancha Roja de Júpiter. Neptuno también tiene un sistema de anillos oscuros y delgados.",
        },
      ];

      planetData.forEach((data) => {
        const geometry = new THREE.SphereGeometry(data.radius, 32, 32);
        const textureLoader = new THREE.TextureLoader();
        const material = new THREE.MeshBasicMaterial({
          map: textureLoader.load(data.texture),
        }); // Usar la textura correspondiente
        const planet = new THREE.Mesh(geometry, material);

        // Posicionar el planeta en su órbita
        planet.position.x = data.distance;
        planet.rotationSpeed = data.rotationSpeed; // Guardar velocidad de rotación
        planet.userData = data; // Guardar información del planeta
        orbitGroup.add(planet); // Agregar el planeta al grupo de órbita
        planets.push(planet);

        // Agregar anillos a Saturno
        if (data.name === "Saturno") {
          const ringGeometry = new THREE.RingGeometry(1.1, 1.8, 32);
          const ringMaterial = new THREE.MeshBasicMaterial({
            map: textureLoader.load(anillos), // Puedes usar otra textura para los anillos
            side: THREE.DoubleSide,
            transparent: true,
            opacity: 0.5,
          });
          const ring = new THREE.Mesh(ringGeometry, ringMaterial);
          ring.rotation.x = -Math.PI / 2; // Rotar los anillos para que estén planos
          planet.add(ring); // Añadir el anillo al planeta
        }

        // Crear órbita como línea imaginaria
        const orbitGeometry = new THREE.RingGeometry(
          data.distance - 0.01,
          data.distance + 0.01,
          64
        );
        const orbitMaterial = new THREE.MeshBasicMaterial({
          color: 0xffffff,
          side: THREE.DoubleSide,
        });
        const orbit = new THREE.Mesh(orbitGeometry, orbitMaterial);
        orbit.rotation.x = Math.PI / 2; // Alinear con el plano de la órbita
        scene.add(orbit);
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
        isRotating.value = false; // Detener la rotación del sistema solar
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

        if (distanceToPlanet > 5) {
          // Continuar acercándose hasta llegar cerca del planeta
          camera.position.lerp(
            targetPosition.clone().add(new THREE.Vector3(0, 0, 5)),
            zoomSpeed
          ); // Acercar a 5 unidades del planeta
          controls.target.copy(targetPosition); // Centrar controles en el planeta
          controls.update();
        } else {
          // Después de acercarse, habilitar la rotación de la vista 360 grados
          controls.enableZoom = true; // Habilitar zoom para la vista de 360 grados
          zoomIn = true; // Desactivar zoom en este estado
        }
      }
    };

    // Función para manejar la navegación
const navigateToPlanet = () => {
  if (targetPlanet) {
  const targetPosition = new THREE.Vector3();
  targetPlanet.getWorldPosition(targetPosition); // Obtener la posición global del planeta

  // Mover la cámara hacia el planeta
  const distanceToPlanet = targetPosition.distanceTo(camera.position);
  const zoomSpeed = 0.2; // Reducir la velocidad de acercamiento para un movimiento más lento

  if (distanceToPlanet > -100) { 
    // Continuar acercándose hacia el centro del planeta con un desplazamiento más pequeño
    camera.position.lerp(
      targetPosition.clone().sub(new THREE.Vector3(0, 0, 100)), // Reducir el desplazamiento a 2 para un acercamiento más suave
      zoomSpeed
    );
    controls.target.copy(targetPosition); // Centrar controles en el planeta
    controls.update();
  }
}


  if (selectedPlanet.value) {
    // Esperar 2 segundos antes de cambiar de página
    setTimeout(() => {
      // Navegar a la ruta específica del planeta seleccionado después de la pausa
      router.push({
        path: `/planets/${selectedPlanet.value.name.toLowerCase()}`,
      });
    }, 2000); // Espera de 2000 milisegundos (2 segundos)
  }
};




    const resetView = () => {
      const sunPosition = new THREE.Vector3(0, 0, 0); // Posición del Sol
      const originalCameraPosition = new THREE.Vector3(0, 0, 70); // Posición inicial de la cámara

      let t = 0; // Tiempo de interpolación (0 a 1)

      // Asegurar que el Sol sea el objetivo
      targetPlanet = sun; // Asignar el Sol como targetPlanet
      controls.target.copy(sunPosition); // Enfocar la cámara hacia el Sol

      // Crear una función de animación para alejarse del planeta y enfocar el Sol
      const zoomOutAnimation = () => {
        if (t < 1) {
          t += 0.02; // Velocidad de la animación

          // Interpolar la posición de la cámara hacia la posición original (alejamiento)
          camera.position.lerp(originalCameraPosition, t);

          // Asegurar que la cámara enfoque el Sol durante la animación
          controls.target.copy(sunPosition);

          // Seguir llamando a la función hasta que el t alcance 1
          requestAnimationFrame(zoomOutAnimation);
        } else {
          // Cuando termine la animación, simplemente enfocar el Sol sin mostrar info-panel
          selectedPlanet.value = null; // No mostrar info-panel del Sol
          targetPlanet = null; // Eliminar el planeta objetivo
          isRotating.value = true; // Reiniciar la rotación del sistema
          controls.update(); // Actualizar controles
        }
      };

      // Iniciar la animación
      zoomOutAnimation();
    };

    const animate = () => {
      requestAnimationFrame(animate);

      if (isRotating.value) {
        // Actualizar la rotación de cada planeta individualmente
        planets.forEach((planet) => {
          const data = planet.userData;

          // Usamos acumuladores para el ángulo de órbita
          if (!planet.userData.orbitAngle) {
            planet.userData.orbitAngle = 0; // Inicializamos el ángulo de órbita si no existe
          }

          // Incrementamos el ángulo de órbita basándonos en la velocidad de rotación
          planet.userData.orbitAngle +=
            data.rotationSpeed * data.orbitDirection; // Multiplicamos por la dirección de la órbita

          // Calculamos las posiciones X y Z basándonos en el ángulo de órbita
          const orbitX = data.distance * Math.cos(planet.userData.orbitAngle);
          const orbitZ = data.distance * Math.sin(planet.userData.orbitAngle);

          // Aplicamos la inclinación de la órbita y actualizamos la posición del planeta
          planet.position.set(
            orbitX,
            data.distance * Math.sin((data.orbitInclination * Math.PI) / 180), // Inclinación en el eje Y
            orbitZ
          );

          // Rotación del planeta sobre su propio eje
          planet.rotation.y += data.rotationSpeed * 0.1; // Ajustar la velocidad de rotación sobre su propio eje
        });
      }

      if (zoomIn) {
        moveToPlanet(); // Manejar el movimiento de acercamiento al planeta
      }

      controls.update(); // Actualizar controles
      renderer.render(scene, camera); // Renderizar la escena
    };

    onMounted(() => {
      showModal.value = true; // Asegurarse de que el modal esté activo al montar la página
      initScene();
      addPlanets();
      animate();

      const closeModal = () => {
        console.log("Modal closed"); // Verificar si se está cerrando correctamente
        showModal.value = false; // Ocultar el modal al cerrar
      };
    });

    onBeforeUnmount(() => {
      window.removeEventListener("resize", onWindowResize);
      renderer.dispose(); // Limpiar recursos
    });

    return {
      showModal,
      closeModal,
      isRotating,
      goBack,
      toggleRotation,
      canvasContainer,
      selectedPlanet,
      resetView,
      navigateToPlanet,
    };
  },
};
</script>

<style>
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 50px; /* Asegúrate de que la altura sea suficiente */
  background-color: rgba(0, 0, 50, 0.8); /* Fondo oscuro */
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  color: white;
  z-index: 1001; /* Asegúrate de que esté encima de otros elementos */
}

.top-bar h1 {
  font-size: 1.5rem;
  text-align: center;
  flex: 1;
}

.nav-button,
.pause-button {
  background-color: #003366; /* Color de fondo */
  color: white;
  border: 2px solid #00ffff; /* Borde brillante */
  padding: 10px;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-button:hover,
.pause-button:hover {
  background-color: #005580;
}

.modal-overlay {
  position: fixed;
  top: 50px; /* Ajustar el cuadro emergente debajo de la barra superior */
  left: 0;
  width: 100vw;
  height: calc(100vh - 50px); /* Ajustar la altura para evitar que se desborde */
  background-color: rgba(0, 0, 0, 0.7); /* Fondo oscuro semitransparente */
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Alinear en la parte superior */
  z-index: 1000;
}

.modal-content {
  background-color: rgba(0, 0, 50, 0.8); /* Fondo oscuro */
  padding: 15px 20px; /* Reducir padding para ahorrar espacio */
  border: 2px solid #00ffff; /* Borde brillante estilo neón */
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.7); /* Sombra brillante */
  width: 80vw; /* Limitar el ancho al 80% del viewport */
  max-width: 700px; /* Limitar el ancho máximo */
  max-height: calc(100vh - 100px); /* Limitar la altura total para que siempre se vea */
  text-align: center;
  color: white;
  font-size: 1rem; /* Reducir tamaño de fuente para ajustarse mejor */
}

.modal-content h2 {
  margin-bottom: 10px;
  font-size: 1.3rem; /* Reducir el tamaño del título */
}

.modal-content p {
  margin-bottom: 15px;
  font-size: 0.9rem; /* Reducir el tamaño del texto */
}

.modal-content button {
  background-color: #003366; /* Color de fondo del botón */
  color: white;
  border: 2px solid #00ffff; /* Borde brillante */
  padding: 8px 16px; /* Reducir tamaño del botón */
  border-radius: 8px;
  font-size: 1rem; /* Reducir tamaño del texto en el botón */
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-content button:hover {
  background-color: #005580; /* Cambia el fondo al pasar el cursor */
  transform: scale(1.05);
  box-shadow: 0px 6px 12px rgba(0, 255, 255, 0.8); /* Sombra más intensa en hover */
}

.canvas-container {
  width: 100vw;
  height: 100vh;
  position: relative;
}

.info-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #1a3f5e;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.7);
  color: #ffffff;
  width: 300px;
  font-family: "Arial", sans-serif;
}

.info-panel h2 {
  font-size: 20px;
  margin-bottom: 10px;
  color: #00ff00;
}

.info-panel p {
  font-size: 16px;
  margin-bottom: 20px;
}

button {
  display: inline-block;
  background-color: #007bff;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
