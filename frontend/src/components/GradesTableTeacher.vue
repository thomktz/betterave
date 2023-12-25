<template>
  <v-container class="main-container">
    <v-container>
      <!-- Users Table -->
      <v-data-table
        :headers="headers"
        :items="props.users"
        class="elevation-1"
      >
        <!-- Profile Picture -->
        <template v-slot:item.profile_pic="{ item }">
          <img
            :src="'/' + item.profile_pic"
            alt="Profile Pic"
            class="profile-pic"
          />
        </template>

        <!-- Grades Column with Edit Icon -->
        <template v-slot:item.grades="{ item }">
          <div>
            {{ item.grades }}
            <v-icon
              @click="editGrade(item)"
              class="icon-pencil"
            >
              mdi-pencil
            </v-icon>
          </div>
        </template>
      </v-data-table>
    </v-container>

    <!-- Dialog for Editing Grade -->
    <v-dialog v-model="dialogVisible" max-width="500px">
      <v-card>
        <v-card-title>Edit Grade</v-card-title>
        <v-card-text>
          <v-text-field v-model="newGrade" label="New Grade"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="saveGrade" color="primary">Save</v-btn>
          <v-btn @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { defineProps, ref } from 'vue';
import { apiClient } from "@/apiConfig";

const props = defineProps({
  users: Array,
  classId: Number, // Declare classId as a prop
});

const headers = [
  { title: "", value: "profile_pic", sortable: false },
  { title: "Surname", value: "surname" },
  { title: "Name", value: "name" },
  { title: "Level", value: "level" },
  { title: "Email", value: "email" },
  { title: "Grades", value: "grades" },
];

const dialogVisible = ref(false);
const newGrade = ref(null);
const selectedUser = ref(null);

const editGrade = (user) => {
  selectedUser.value = user;
  newGrade.value = user.grades;
  dialogVisible.value = true;
};

const saveGrade = async () => {
  try {
    if (selectedUser.value) {
      console.log("classId:", props.classId);
      console.log("selectedUser:", selectedUser.value);
      console.log("newGrade:", newGrade.value);

      // Call your API to save the new grade for selectedUser
      const response = await apiClient.put(`/users/${props.classId}/grades/${selectedUser.value.user_id}`, {
        grade: newGrade.value,
      });

      console.log("API Response:", response);

      // Check if the API call was successful
      if (response.status === 200) {
        // Update the local user data with the new grade
        selectedUser.value.grades = newGrade.value;

        // Close the dialog
        closeDialog();
      } else {
        // Handle the case where the API call was not successful
        console.error("Error updating grade:", response.data);
        // Display an error message or show a notification
      }
    }
  } catch (error) {
    console.error("Error updating grade:", error);
    // Handle the error, e.g., show an error message or notification
  }
};

const closeDialog = () => {
  selectedUser.value = null;
  newGrade.value = null;
  dialogVisible.value = false;
};
</script>

<style scoped>
.main-container {
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  padding: 0;
  margin-top: 20px;
  border-radius: 15px;
}

.profile-pic {
  width: 50px;
  height: 50px;
  border-radius: 20%;
}

.icon-pencil {
  cursor: pointer;
  margin-left: 5px;
}
</style>
