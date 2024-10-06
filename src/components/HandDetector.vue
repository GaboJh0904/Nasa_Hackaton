<template>
  <div class="text-center mt-5">
    <button @click="startMouse" class="btn btn-primary m-2">Iniciar Mouse Virtual</button>
    <button @click="stopMouse" class="btn btn-danger m-2">Cancelar Mouse Virtual</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    startMouse() {
      axios.get('http://localhost:5000/start_mouse')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    stopMouse() {
      axios.get('http://localhost:5000/stop_mouse')
        .then(response => {
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>

