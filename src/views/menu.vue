<template>
  <div class="h-screen w-full relative fondo-imagen flex justify-center items-center">
    <!-- Título central -->
    <div class="contenedor absolute top-1/4 left-1/2 transform -translate-x-1/2">
      <h1 class="text-white text-4xl font-extrabold text-center">Modulos Educativos</h1>
    </div>

    <!-- Cuadro con botones alineados a la derecha, centrado verticalmente -->
    <div class="botones-contener absolute right-10 top-1/2 transform -translate-y-1/2">
      <div class="space-y-4 w-full max-w-md">
        <div class="bg-gray-100 p-4 rounded shadow-md">
          <button class="w-full py-3 text-center bg-blue-900 text-white border-2 border-gray-400 hover:bg-blue-800 shadow-lg">
            Modulo Primaria
          </button>
        </div>

        <div class="bg-gray-100 p-4 rounded shadow-md">
          <button class="w-full py-3 text-center bg-blue-900 text-white border-2 border-gray-400 hover:bg-blue-800 shadow-lg">
            Modulo Secundaria
          </button>
        </div>

        <div class="bg-gray-100 p-4 rounded shadow-md">
          <button @click="navigateToHome" class="w-full py-3 text-center bg-blue-900 text-white border-2 border-gray-400 hover:bg-blue-800 shadow-lg">
            Modulo Universitario
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    navigateToHome() {
      this.$router.push('/home');
    }
  }
}
</script>

<style scoped>
/* Estilos adicionales para mejorar el diseño */
h1 {
  font-size: 3rem;
  font-weight: bold;
  text-transform: uppercase;
  color: #1e90ff; /* Azul moderado */
  text-shadow: 
    0 0 10px rgba(30, 144, 255, 0.7), /* Resplandor azul */
    0 0 20px rgba(30, 144, 255, 0.5),
    0 0 30px rgba(30, 144, 255, 0.3),
    0 0 40px rgba(30, 144, 255, 0.2),
    2px 2px 8px rgba(0, 0, 0, 0.8), /* Sombra oscura para el borde */
    3px 3px 10px rgba(0, 0, 0, 1); /* Sombra más definida para dar profundidad */
  
  animation: flicker 2s infinite alternate; /* Efecto de parpadeo */
}

/* Animación para simular un parpadeo de luz */
@keyframes flicker {
  0% {
    opacity: 1;
    text-shadow: 
      0 0 10px rgba(30, 144, 255, 0.7),
      0 0 20px rgba(30, 144, 255, 0.5),
      0 0 30px rgba(30, 144, 255, 0.3),
      0 0 40px rgba(30, 144, 255, 0.2),
      2px 2px 8px rgba(0, 0, 0, 0.8), /* Sombra oscura */
      3px 3px 10px rgba(0, 0, 0, 1); /* Sombra oscura más pronunciada */
  }
  50% {
    opacity: 0.8;
    text-shadow: 
      0 0 5px rgba(30, 144, 255, 0.5),
      0 0 15px rgba(30, 144, 255, 0.4),
      0 0 25px rgba(30, 144, 255, 0.2),
      2px 2px 8px rgba(0, 0, 0, 0.8),
      3px 3px 10px rgba(0, 0, 0, 1);
  }
  100% {
    opacity: 1;
    text-shadow: 
      0 0 10px rgba(30, 144, 255, 0.7),
      0 0 20px rgba(30, 144, 255, 0.5),
      0 0 30px rgba(30, 144, 255, 0.3),
      0 0 40px rgba(30, 144, 255, 0.2),
      2px 2px 8px rgba(0, 0, 0, 0.8),
      3px 3px 10px rgba(0, 0, 0, 1);
  }
}

/* Estilo de los botones con tamaño fijo */
button {
  width: 220px; /* Tamaño fijo de los botones */
  height: 60px; /* Altura fija */
  font-size: 1.2rem; /* Ajuste del tamaño de la fuente */
  color: white;
  background-color: #003366; /* Color de fondo similar al diseño de la imagen */
  border: 2px solid #00ffff; /* Borde brillante */
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.7); /* Sombra para darle profundidad */
  transition: all 0.3s ease;
  text-transform: uppercase; /* Transformación a mayúsculas */
}

/* Efecto hover con aumento de tamaño */
button:hover {
  background-color: #005580; /* Cambia el fondo al pasar el cursor */
  transform: scale(1.05);
  box-shadow: 0px 6px 12px rgba(0, 255, 255, 0.8); /* Sombra más intensa en hover */
}

/* Asegurarse que el fondo ocupe toda la pantalla */
.fondo-imagen {
  display: flex;
  background-image: url('@/assets/fondo.png'); /* Ajusta la ruta si es necesario */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh; /* Ocupa toda la altura de la ventana */
}

.bg-gray-900 {
  backdrop-filter: blur(5px); /* Efecto de desenfoque */
}

/* Espaciado vertical entre los botones */
.space-y-4 > * + * {
  margin-top: 1rem;
}

.contenedor {
  top: 5%; /* Ajuste para que esté en la parte superior */
  left: 50%; /* Centrado horizontalmente */
  transform: translateX(-50%); /* Asegura que quede centrado horizontalmente */
  position: absolute; /* Para poder mover el contenedor en la pantalla */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

/* Estilo del contenedor que aloja los botones */
.botones-contener {
  position: absolute;
  top: 50%; /* Centrado verticalmente */
  right: -8%; /* Centrado horizontalmente */
  transform: translate(-50%, -50%); /* Traducción para centrar en ambos ejes */
  background-color: rgba(0, 0, 50, 0.8); /* Fondo oscuro similar a la imagen */
  padding: 20px;
  border: 2px solid #00ffff; /* Borde brillante estilo neón */
  border-radius: 10px;
  box-shadow: 0px 0px 15px rgba(0, 255, 255, 0.7); /* Sombra brillante */
  max-width: 250px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center; /* Asegura que los botones estén centrados dentro del contenedor */
}

</style>
