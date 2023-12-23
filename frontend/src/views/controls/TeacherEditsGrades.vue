<template>
  <v-container class="fill-height" fluid>
    <GradesTable
      :users="users"
      @delete-user="deleteUser"
      @add-user="addUser"
      @edit-user="editUser"
    />
  </v-container>
</template>

<script>
import { apiClient } from "@/apiConfig";
import GradesTable from "@/components/GradesTable.vue";
import { ref, onMounted } from "vue";

export default {
  components: {
    GradesTable,
  },
  setup() {
    const users = ref([]); // Create a reactive reference for the users list

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
          const response = await apiClient.get(`/users/studentlist/${classId.value}`);
          users.value = response.data;
        }
      } catch (error) {
        console.error("Error fetching users:", error);
        // Handle error, e.g., show notification
      }
    };

    // Delete user by ID
    const deleteUser = async (user_id) => {
      try {
        await apiClient.delete(`/users/${user_id}`);
        users.value = users.value.filter((user) => user.user_id !== user_id);
      } catch (error) {
        console.error("Error deleting user:", error);
        // Handle error, e.g., show notification
      }
    };

    // Add a new user
    const addUser = async (userData) => {
      try {
        const response = await apiClient.post("/users", userData);
        users.value.push(response.data);
      } catch (error) {
        console.error("Error adding user:", error);
      }
    };

    // Edit existing user details
    const editUser = async (userData) => {
      try {
        await apiClient.put(`/users/${userData.user_id}`, userData);
        // Find and update the user in the list
        const index = users.value.findIndex(
          (user) => user.user_id === userData.user_id,
        );
        if (index !== -1) {
          users.value[index] = { ...users.value[index], ...userData };
        }
      } catch (error) {
        console.error("Error editing user:", error);
      }
    };

    onMounted(fetchUsers);
    return {
      users,
      classId,
      deleteUser,
      addUser,
      editUser,
    };
  },
};
</script>

<style>
/* Add your styles here */
</style>