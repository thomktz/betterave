import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import HomePage from '../views/HomePage.vue'
import Photochart from '../views/Photochart.vue'
import axios from 'axios';

const routes = [
  {
    path: '/',
    name: 'homepage',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/photochart',
    name: 'Photochart',
    component: Photochart,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  // If the user is navigating to the login page, just continue.
  console.log(to.name)
  if (to.name === 'Login') {
    next();
    return;
  }

  // Otherwise, check if the user is authenticated.
  try {
    console.log("Fetching auth")
    const response = await axios.get('http://127.0.0.1:5000/check-auth', {
      withCredentials: true,
    });
    console.log(response.data)
    if (response.data.status === 'authenticated') {
      next();
    } else {
      next({ name: 'Login' });  // Redirect to login
    }
  } catch (error) {
    console.log(error)
    next({ name: 'Login' });  // Redirect to login in case of error
  }
});

export default router
