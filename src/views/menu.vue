<template>
    <div class="h-screen w-full relative fondo-imagen">
      <!-- Título central superior -->
      <div class="absolute top-0 left-0 w-full flex justify-center py-8">
        <h1 class="text-white text-4xl font-extrabold">Modulos Educativos</h1>
      </div>
  
      <!-- Menú en el lado izquierdo -->
      <div class="absolute left-10 top-1/4 space-y-4">
        <button class="w-64 py-3 text-left px-6 bg-gray-700 text-white opacity-50 cursor-not-allowed border-l-4 border-gray-500">
          Modulo Primaria
        </button>
        <button class="w-64 py-3 text-left px-6 bg-gray-700 text-white opacity-50 cursor-not-allowed border-l-4 border-gray-500">
          Modulo Secundaria
        </button>
        <button @click="navigateToHome" class="w-64 py-3 text-left px-6 bg-blue-600 text-white hover:bg-blue-700 border-l-4 border-blue-400">
          Modulo Universitario
        </button>
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
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
  }
  
  button {
    font-size: 1.1rem;
    transition: all 0.3s ease;
  }
  
  button:hover {
    transform: scale(1.05);
  }
  
  /* Asegurarse que el fondo ocupe toda la pantalla */
  .fondo-imagen {
    background-image: url('@/assets/fondo.png'); /* Ajusta la ruta si es necesario */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    height: 100vh; /* Ocupa toda la altura de la ventana */
  }
  </style>
  