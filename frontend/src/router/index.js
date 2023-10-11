import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import HomePage from '../views/HomePage.vue'
import ClassPage from '../views/ClassPage.vue'
import MainLayout from '../views/MainLayout.vue'  // <-- make sure the path is correct
import axios from 'axios';

const routes = [
  {
    path: '/',
    component: MainLayout, // MainLayout becomes the default layout for HomePage and ClassPage
    children: [
      {
        path: '',  // empty path as this will match the root path within MainLayout
        name: 'homepage',
        component: HomePage
      },
      {
        path: 'class/:classId', // dynamic segment for class id
        name: 'class-details',
        component: ClassPage
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  // If the user is navigating to the login page, just continue.
  if (to.name === 'Login') {
    next();
    return;
  }

  // Otherwise, check if the user is authenticated.
  try {
    const response = await axios.get('http://127.0.0.1:5000/check-auth', {
      withCredentials: true,
    });
    if (response.data.status === 'authenticated') {
      next();
    } else {
      next({ name: 'Login' });  // Redirect to login
    }
  } catch (error) {
    console.log(error);
    next({ name: 'Login' });  // Redirect to login in case of error
  }
});

export default router;
