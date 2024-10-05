import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Importa el enrutador

const app = createApp(App);

app.use(router); // Inyecta el router en la aplicación

app.mount('#app');
