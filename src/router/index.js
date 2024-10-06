import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/home.vue'; // Página del sistema solar (anteriormente App.vue)
import Earth from '@/views/planets/earth.vue'; // La página del planeta Tierra
import Jupiter from "@/views/planets/jupiter.vue";
import Mars from "@/views/planets/mars.vue";
import Mercury from "@/views/planets/mercury.vue";
import Neptune from "@/views/planets/neptune.vue";
import Saturn from "@/views/planets/saturn.vue";
import Uranus from "@/views/planets/uranus.vue";
import Venus from "@/views/planets/venus.vue";

const routes = [
  { path: '/', component: Home }, // Página principal con el mapa del sistema solar
  { path: '/planets/Tierra', component: Earth }, // Ruta para la página de la Tierra
  { path: '/planets/Júpiter', component: Jupiter }, // Ruta para la página de la Tierra
  { path: '/planets/Marte', component: Mars }, // Ruta para la página de la Tierra
  { path: '/planets/Mercurio', component: Mercury }, // Ruta para la página de la Tierra
  { path: '/planets/Neptuno', component: Neptune }, // Ruta para la página de la Tierra
  { path: '/planets/Saturno', component: Saturn }, // Ruta para la página de la Tierra
  { path: '/planets/Urano', component: Uranus }, // Ruta para la página de la Tierra
  { path: '/planets/Venus', component: Venus }, // Ruta para la página de la Tierra
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
