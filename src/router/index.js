import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/home.vue'; // Página del sistema solar (anteriormente App.vue)
import Earth from '@/views/planets/earth.vue'; // La página del planeta Tierra

const routes = [
  { path: '/', component: Home }, // Página principal con el mapa del sistema solar
  { path: '/planets/Tierra', component: Earth }, // Ruta para la página de la Tierra
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
