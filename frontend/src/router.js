import { createRouter, createWebHistory } from 'vue-router';
import LoginView from './components/LoginView.vue';
import HomePage from './components/HomePage.vue';

const routes = [
    { path: '/', name: 'HomePage', component: HomePage }, 
    { path: '/login', name: 'LoginView', component: LoginView },
  ];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

