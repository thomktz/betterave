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
          <img :src="'/' + item.profile_pic" alt="Profile Pic" class="profile-pic" />
        </template>

        <!-- Actions (Edit & Delete) -->
        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            class="mr-2"
            @click="emitEditUser(item)"
          >
            mdi-pencil
          </v-icon>
          <v-icon
            small
            @click="emitDeleteUser(item.user_id)"
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </v-container>
  </v-container>

  <!-- Add User Dialog -->
  <v-dialog v-model="showAddDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Add New User</span>
      </v-card-title>
      <v-card-text>
        <!-- Add User Form -->
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="newUser.name" label="Name" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="newUser.surname" label="Surname" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="newUser.email" label="Email" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="newUser.level"
                :items="['1A', '2A', '3A', 'N/A']"
                label="Level"
                required
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="newUser.user_type"
                :items="['asso', 'student', 'teacher', 'admin']"
                label="User Type"
                required
              ></v-select>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="showAddDialog = false">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="handleAddUser">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- Edit User Dialog -->
  <v-dialog v-model="showEditDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Edit User Details</span>
      </v-card-title>
      <v-card-text>
        <!-- Edit User Form -->
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="selectedUser.name" label="Name" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="selectedUser.surname" label="Surname" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="selectedUser.email" label="Email" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="selectedUser.level"
                :items="['1A', '2A', '3A', 'N/A']"
                label="Level"
                required
              ></v-select>
            </v-col>
            <v-col cols="12">
              <v-select
                v-model="selectedUser.user_type"
                :items="['asso', 'student', 'teacher', 'admin']"
                label="User Type"
                required
              ></v-select>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="showEditDialog = false">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="handleEditUser">Save</v-btn>
        <v-btn color="green" text @click="navigateToEditClasses(selectedUser.user_id)">
          Edit classes
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue';
import router from '@/router';

// Props
const props = defineProps({
  users: Array
});

// Reactive state for dialogs
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const levelFilter = ref('');
const typeFilter = ref('');
const newUser = ref({ name: '', surname: '' }); // Initialize with empty fields
const selectedUser = ref({}); // Initialize the selected user for editing
const search = ref('');
const headers = ref([
  { title: '', value: 'profile_pic', sortable: false },
  { title: 'Surname', value: 'surname' },
  { title: 'Name', value: 'name' },
  { title: 'Level', value: 'level' },
  { title: 'Type', value: 'user_type' },
  { title: 'Email', value: 'email' },
  { title: '', value: 'actions', sortable: false },
]);

const filteredUsers = computed(() => {
  return props.users.filter((user) => {
    return (!levelFilter.value || user.level === levelFilter.value) &&
           (!typeFilter.value || user.user_type === typeFilter.value);
  });
});

const navigateToEditClasses = (studentId) => {
  router.push(`/controls/admin/${studentId}`);
};

// Emits
const emit = defineEmits(['delete-user', 'edit-user', 'add-user']);

// Methods for handling emits
const emitDeleteUser = (user_id) => {
  console.log(`Request to delete user with ID: ${user_id}`);
  emit('delete-user', user_id);
};

const emitEditUser = (user) => {
  selectedUser.value = { ...user }; // Make a copy of the user object for editing
  console.log(`Opening edit dialog for user:`, selectedUser.value);
  showEditDialog.value = true; // Show the edit dialog
};

const handleEditUser = () => {
  // Implement your logic to handle user edit
  console.log("Editing user:", selectedUser.value);
  emit('edit-user', selectedUser.value);
  showEditDialog.value = false; // Close the dialog
};

const handleAddUser = () => {
  // Implement your logic to handle add user
  console.log("Adding new user:", newUser.value);
  emit('add-user', newUser.value);
  showAddDialog.value = false; // Close the dialog after emitting the event
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
    width: 56px; /* This is the standard size for an icon button */
    height: 56px;
    background-color: #1d958b; /* deep-purple accent-4 */
    border-radius: 50%;
    transition: background-color 0.3s, transform 0.3s;
    cursor: pointer;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.custom-circle-btn:hover {
    background-color: #3bc8bc; /* A lighter deep-purple for hover effect */
    transform: scale(1.1); /* Scale effect on hover */
}

.custom-circle-btn v-icon {
    color: white; /* Ensure the icon is white */
    transition: transform 0.3s;
}

.custom-circle-btn:hover v-icon {
    transform: rotate(90deg); /* Optional: adds a rotation to the plus icon on hover */
}

.px-2 {
  margin-bottom: 5px;
}

</style>