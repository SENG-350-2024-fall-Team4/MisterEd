// main.js
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// Import Bootstrap CSS and JS bundle
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';

const app = createApp(App);

// Initialize Pinia and Router
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.mount('#app');
