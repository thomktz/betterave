<template>
  <v-container class="main-container">
    <v-container>
      <v-row align="stretch" class="px-2">
        <!-- Add User Button -->
        <v-col cols="auto" class="d-flex align-center justify-space-around">
          <div class="custom-circle-btn" @click="showAddDialog = true">
            <v-icon>mdi-plus</v-icon>
          </div>
        </v-col>

        <!-- Spacer -->
        <v-spacer></v-spacer>

        <!-- Level Filter -->
        <v-col cols="12" sm="3" class="mx-1">
          <v-select
            v-model="levelFilter"
            :items="['1A', '2A', '3A', 'N/A']"
            label="Filter by Level"
            clearable
            hide-details
          ></v-select>
        </v-col>

        <!-- Spacer -->
        <v-spacer></v-spacer>

        <!-- Type Filter -->
        <v-col cols="12" sm="3" class="mx-1">
          <v-select
            v-model="typeFilter"
            :items="['student', 'asso', 'teacher', 'admin']"
            label="Filter by Type"
            clearable
            hide-details
          ></v-select>
        </v-col>

        <!-- Spacer -->
        <v-spacer></v-spacer>

        <!-- Search Field -->
        <v-col cols="12" sm="4" class="mx-1">
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-row>

      <!-- Users Table -->
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :search="search"
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

        <!-- Grades Column -->
        <template v-slot:item.grades="{ item }">
          <v-text-field
            v-model="item.grades"
            @input="handleEditGrades(item)"
            outlined
            dense
          ></v-text-field>
        </template>

        <!-- Actions (Edit & Delete) -->
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="emitEditUser(item)">
            mdi-pencil
          </v-icon>
          <v-icon small @click="emitDeleteUser(item.user_id)">
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </v-container>
  </v-container>

  <!-- Add User Dialog -->
  <v-dialog v-model="showAddDialog" persistent max-width="600px">
    <!-- ... (rest of your add user dialog code) -->
  </v-dialog>

  <!-- Edit User Dialog -->
  <v-dialog v-model="showEditDialog" persistent max-width="600px">
    <!-- ... (rest of your edit user dialog code) -->
  </v-dialog>
</template>

<script setup>
import { ref, computed } from "vue";
import router from "@/router";

const props = defineProps({
  users: Array,
});

const showAddDialog = ref(false);
const showEditDialog = ref(false);
const levelFilter = ref("");
const typeFilter = ref("");
const newUser = ref({ name: "", surname: "" });
const selectedUser = ref({});
const search = ref("");
const headers = ref([
  { title: "", value: "profile_pic", sortable: false },
  { title: "Surname", value: "surname" },
  { title: "Name", value: "name" },
  { title: "Level", value: "level" },
  { title: "Type", value: "user_type" },
  { title: "Email", value: "email" },
  { title: "Grades", value: "grades" }, // Fixed typo here
  { title: "", value: "actions", sortable: false },
]);

const filteredUsers = computed(() => {
  return props.users.filter((user) => {
    return (
      (!levelFilter.value || user.level === levelFilter.value) &&
      (!typeFilter.value || user.user_type === typeFilter.value)
    );
  });
});

const navigateToEditClasses = (studentId) => {
  router.push(`/controls/admin/${studentId}`);
};

const emit = defineEmits(["delete-user", "edit-user", "add-user"]);

const emitDeleteUser = (user_id) => {
  emit("delete-user", user_id);
};

const emitEditUser = (user) => {
  selectedUser.value = { ...user };
  showEditDialog.value = true;
};

const handleEditUser = () => {
  console.log("Editing user:", selectedUser.value);
  emit("edit-user", selectedUser.value);
  showEditDialog.value = false;
};

const handleAddUser = () => {
  console.log("Adding new user:", newUser.value);
  emit("add-user", newUser.value);
  showAddDialog.value = false;
};

const handleEditGrades = (user) => {
  console.log("Editing grades for user:", user);
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

.custom-circle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background-color: #1d958b;
  border-radius: 50%;
  transition: background-color 0.3s, transform 0.3s;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.custom-circle-btn:hover {
  background-color: #3bc8bc;
  transform: scale(1.1);
}

.custom-circle-btn v-icon {
  color: white;
  transition: transform 0.3s;
}

.custom-circle-btn:hover v-icon {
  transform: rotate(90deg);
}

.px-2 {
  margin-bottom: 5px;
}
</style>