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
        
        <!-- Grades Column -->
        <template v-slot:item.grades="{ item }">
          <div>{{ item.grades }}</div>
        </template>
      </v-data-table>
    </v-container>
  </v-container>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  users: Array,
});

const headers = [
  { title: "", value: "profile_pic", sortable: false },
  { title: "Surname", value: "surname" },
  { title: "Name", value: "name" },
  { title: "Level", value: "level" },
  { title: "Email", value: "email" },
  { title: "Grades", value: "grades" },
];
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
</style>
