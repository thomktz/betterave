<template>
    <div class="profile-pill" @mouseover="showDropdown = true" @mouseleave="showDropdown = false">
      <div class="email-with-icon">
        <img src="/default-profile.png" alt="Profile Icon" class="profile-icon" />
        <span>{{ userEmail }}</span>
      </div>
      <div v-if="showDropdown" class="dropdown-content">
        <button @click="logout">Logout</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      userEmail: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        showDropdown: false
      };
    },
    methods: {
      async logout() {
        try {
          await axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true });
          this.$router.push({ name: 'Login' });
        } catch (error) {
          console.error("There was an error logging out:", error);
        }
      }
    }
  }
  </script>