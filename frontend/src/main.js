import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles/main.scss'
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
import VueSplide from '@splidejs/splide';
import router from './router'
import store from '../store';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'




// Register Font Awesome icons
library.add(fas);
library.add(far);
library.add(fab);

const vuetify = createVuetify({
    components,
    directives,
  })

const baseMediaUrl = '16.16.128.80:8000';
const baseUrl = 'http://16.16.128.80:8000/shop';

// Create the Vue app instance
const app = createApp(App);

app.config.globalProperties.$baseMediaUrl = baseMediaUrl;
app.config.globalProperties.$baseUrl = baseUrl;

// Register the Font Awesome component globally
app.component('font-awesome-icon', FontAwesomeIcon);
app.component('VueSplide', VueSplide );
app.use(router);
app.use(store);
app.use(vuetify)

// Mount the app to the DOM
app.mount('#app');