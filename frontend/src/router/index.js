import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import HomePage from "../views/HomePage.vue";
import Photochart from "../views/Photochart.vue";
import ClassPage from "../views/ClassPage.vue";
import MainLayout from "../views/MainLayout.vue";
import AssoList from "../views/AssoList.vue";
import StudentControls from "../views/controls/StudentControls.vue";
import StudentGrades from "../views/controls/StudentGrades.vue";
import TeacherGrades from "../views/controls/TeacherGrades.vue";
import AssoControls from "../views/controls/AssoControls.vue";
import AdminControls from "../views/controls/AdminControls.vue";
import EditClasses from "../views/controls/EditClasses.vue";
import { apiClient } from "@/apiConfig";

const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "homepage",
        component: HomePage,
      },
      {
        path: "class/:class_id", // dynamic segment for class id
        name: "class-details",
        component: ClassPage,
      },
      {
        path: "/photochart",
        name: "Photochart",
        component: Photochart,
      },
      {
        path: "/assolist",
        name: "asso-list",
        component: AssoList,
      },
      {
        path: "/controls/student",
        name: "student-controls",
        component: StudentControls,
      },
      {
        path: "/controls/student",
        name: "student-grades",
        component: StudentGrades,
      },
      {
        path: "/controls/teacher",
        name: "teacher-grades",
        component: TeacherGrades,
      }
      ,
      {
        path: "/controls/asso",
        name: "asso-controls",
        component: AssoControls,
        meta: { requiresAuth: true, role: "asso" },
      },
      {
        path: "/controls/admin",
        name: "admin-controls",
        component: AdminControls,
        meta: { requiresAuth: true, role: "admin" },
      },
      {
        path: "/controls/admin/:student_id",
        name: "EditClasses",
        component: EditClasses,
        meta: { requiresAuth: true, role: "admin" },
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  // If the user is navigating to the login page or any public page, just continue.
  if (to.name === "Login" || to.meta.public) {
    next();
    return;
  }
  // Otherwise, check if the user is authenticated and has the required role.
  try {
    const response = await apiClient.get("/auth/check-auth");

    const userAuthenticated = response.data.status === "authenticated";
    const userRole = response.data.role;

    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
      // If the user is not authenticated, redirect to login.
      if (!userAuthenticated) {
        next({ name: "Login" });
        return;
      }

      // If the route requires a role, check if the user has it or user is admin
      if (to.meta.role && userRole !== to.meta.role && userRole !== "admin") {
        // If the user does not have the role, redirect to the homepage or an error page.
        next({ name: "homepage" }); // or your error route name
        return;
      }
    }
    // If all checks pass, proceed to the route.
    next();
  } catch (error) {
    console.log(error);
    // In case of error, redirect to the login.
    next({ name: "Login" });
  }
});

export default router;
