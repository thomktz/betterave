<template>
  <v-container class="fill-height" fluid>
    <GradesTable :users="usersWithGrades" :classId="classId" />
  </v-container>
</template>

<script>
import { apiClient } from "@/apiConfig";
import GradesTable from "@/components/GradesTableTeacher.vue";
import { ref, onMounted } from "vue";

export default {
  components: {
    GradesTable,
  },
  setup() {
    const usersWithGrades = ref([]); // Create a reactive reference for users with grades

    // Extract class_id from the URL
    const classId = ref(null);
    const pathSegments = window.location.pathname.split("/");
    const classIndex = pathSegments.indexOf("class");

    if (classIndex !== -1 && pathSegments[classIndex + 1]) {
      classId.value = parseInt(pathSegments[classIndex + 1]);
    }

    // Fetch users from the API based on class_id
    const fetchUsers = async () => {
      try {
        if (classId.value) {
          const response = await apiClient.get(
            `/users/studentlist/${classId.value}`,
          );
          const users = response.data;

          // Fetch grades for each student and create new objects
          const usersWithGradesArray = await Promise.all(
            users.map(async (user) => {
              const gradesResponse = await apiClient.get(
                `/users/${classId.value}/grades/${user.user_id}`,
              );
              const grade =
                gradesResponse.data.length > 0
                  ? gradesResponse.data[0].grade
                  : "-";
              return { ...user, grades: grade };
            }),
          );

          usersWithGrades.value = usersWithGradesArray;
        }
      } catch (error) {
        console.error("Error fetching users:", error);
        // Handle error, e.g., show notification
      }
    };

    onMounted(fetchUsers);
    return {
      usersWithGrades,
      classId,
    };
  },
};
</script>

<style></style>
