<template>
    <div>
      <header class="header">
        <router-link to="/">
            <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" title="Home page" />
        </router-link>
        <h1>Hello, {{ user.name }}</h1>
        <ProfilePill :userEmail="user.email" />
      </header>
      <router-view />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import ProfilePill from '@/components/ProfilePill.vue';
  
  export default {
    components: {
      ProfilePill
    },
    data() {
      return {
        user: {
          name: '',
          email: ''
        },
      };
    },
    async mounted() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/profile', { withCredentials: true });
        this.user = response.data;
      } catch (error) {
        console.error("There was an error fetching user data:", error);
      }
    }
  };
  </script>
  
  <style>
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    background-color: #f5f5f5; /* Background color for the square */
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* subtle shadow for modern effect */
  }
  
  .logo {
    height: 150px;
    width: auto;
  }
  
  h1 {
    font-size: 2rem;
    font-weight: 700; 
  }

.fill-height {
  min-height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
  </style>
  