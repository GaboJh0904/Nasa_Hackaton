<template>
  <div class="text-center mt-5">
    <h3>Selecciona una imagen:</h3>
    <div class="image-gallery">
      <!-- Lista de imágenes -->
      <img
        v-for="(image, index) in images"
        :key="index"
        :src="image.src"
        :alt="image.alt"
        :class="{ selected: selectedImage === image.name }"
        @click="selectImage(image.name)"
        class="selectable-image"
      />
    </div>

    <!-- Botones para iniciar y cancelar el mouse virtual -->
    <button  class="btn btn-primary m-2">
      Iniciar Mouse Virtual
    </button>
    <button  class="btn btn-danger m-2">
      Cancelar Mouse Virtual
    </button>

    <!-- Mensaje de estado -->
    <p v-if="statusMessage" :class="statusClass">{{ statusMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedImage: "", // Almacena la imagen seleccionada
      images: [
        { name: "amongUs", src: "python/casco/amongUs.png", alt: "Imagen 1" },
        {
          name: "astronauta",
          src: "python/casco/astronauta.png",
          alt: "Imagen 2",
        },
        {
          name: "llamaProfile",
          src: "python/casco/llamaProfile.png",
          alt: "Imagen 3",
        },
      ],
      statusMessage: "",  // Mensaje para mostrar el estado de las operaciones
      statusClass: "",    // Clase para el estilo del mensaje
    };
  },
  methods: {
    // Selecciona la imagen cuando se presiona sobre ella
    selectImage(imageName) {
      this.selectedImage = imageName;
      this.statusMessage = "";  // Limpiar mensaje de estado al seleccionar imagen
    },
    // Maneja las respuestas del servidor
    handleResponse(response) {
      this.statusMessage = response.data.status; // Mensaje del servidor
      this.statusClass = "text-success";         // Clase de éxito
    },
    // Maneja errores de las solicitudes
    handleError(error) {
      this.statusMessage = error.response.data.message || "Error inesperado"; // Mensaje de error
      this.statusClass = "text-danger"; // Clase de error
    },

  },
};
</script>

<style scoped>
.image-gallery {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.selectable-image {
  width: 150px;
  height: 150px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.3s ease;
}

.selectable-image:hover {
  border-color: lightgray;
}

.selected {
  border-color: blue;
}

.text-success {
  color: green; /* Color para mensaje de éxito */
}

.text-danger {
  color: red;   /* Color para mensaje de error */
}
</style>
