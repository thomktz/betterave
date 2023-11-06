import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import HomePage from '../views/HomePage.vue'
import Photochart from '../views/Photochart.vue'
import ClassPage from '../views/ClassPage.vue'
import MainLayout from '../views/MainLayout.vue'
import AssoList from '../views/AssoList.vue';
import AssoControls from '../views/controls/AssoControls.vue'
import TeacherControls from '../views/controls/TeacherControls.vue'
import AdminControls from '../views/controls/AdminControls.vue'
import EditClasses from '../views/controls/EditClasses.vue'
import axios from 'axios';

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '', 
        name: 'homepage',
        component: HomePage
      },
      {
        path: 'class/:classId', // dynamic segment for class id
        name: 'class-details',
        component: ClassPage
      },
      {
        path: '/photochart',
        name: 'Photochart',
        component: Photochart,
      },
      {
        path: '/assolist',
        name: 'asso-list',
        component: AssoList,
      },
      {
        path: '/controls/asso',
        name: 'asso-controls',
        component: AssoControls,
        meta: { requiresAuth: true, role: 'asso' }
      },
      {
        path: '/controls/teacher',
        name: 'teacher-controls',
        component: TeacherControls,
        meta: { requiresAuth: true, role: 'teacher' }
      },
      {
        path: '/controls/admin',
        name: 'admin-controls',
        component: AdminControls,
        meta: { requiresAuth: true, role: 'admin' }
      },
      {
        path: '/controls/admin/:student_id',
        name: 'EditClasses',
        component: EditClasses,
        meta: { requiresAuth: true, role: 'admin' }
      },
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  // If the user is navigating to the login page or any public page, just continue.
  if (to.name === 'Login' || to.meta.public) {
    next();
    return;
  }

  // Otherwise, check if the user is authenticated and has the required role.
  try {
    const response = await axios.get('/check-auth', {
      withCredentials: true,
    });

    const userAuthenticated = response.data.status === 'authenticated';
    const userRole = response.data.role; 

    console.log(userAuthenticated, userRole);

    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
      // If the user is not authenticated, redirect to login.
      if (!userAuthenticated) {
        next({ name: 'Login' });
        return;
      }

      // If the route requires a role, check if the user has it.
      if (to.meta.role && userRole !== to.meta.role) {
        // If the user does not have the role, redirect to the homepage or an error page.
        next({ name: 'homepage' }); // or your error route name
        return;
      }
    }
    console.log('All good to proceed to page!');
    // If all checks pass, proceed to the route.
    next();
  } catch (error) {
    console.log(error);
    // In case of error, redirect to the login.
    next({ name: 'Login' });
  }
});

export default router;
