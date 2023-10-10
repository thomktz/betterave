<template>
  <v-container class="fill-height" fluid>
    <header class="header">
      <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />
      <h1>Hello, {{ user.name }}</h1>
      <ProfilePill :userEmail="user.email" @logout="logout" />
    </header>

    <div class="calendar-container">
      <div class="calendar-box">
        <StudentCalendar />
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios';
import StudentCalendar from '@/components/StudentCalendar.vue';
import ProfilePill from '@/components/ProfilePill.vue';

export default {
  components: {
    StudentCalendar,
    ProfilePill
  },
  data() {
    return {
      user: {
        name: '',
        email: ''
      }
    };
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/profile', { withCredentials: true });
      this.user = response.data;
    } catch (error) {
      console.error("There was an error fetching user data:", error);
    }
  },
  methods: {

  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: #a3cdcf;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 0;
}

.logo {
  height: 150px;
  width: auto;
}

h1 {
  font-size: 2rem;
}

.calendar-container {
  flex: 1;
  display: flex;
  justify-content: flex-end; /* push the calendar to the right */
  padding: 20px; /* Add some spacing from the edges of the screen */
  width: 100%; /* Full width */
}

.calendar-box {
  background-color: #f5f5f5; /* light background color */
  border-radius: 10px; /* rounded corners */
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* subtle shadow for modern effect */
  width: calc(50% - 40px); /* adjust for padding */
  overflow: hidden; /* hide overflow for nested elements to ensure corners are rounded */
  height: 75vh; /* adjust based on your design preference */
}


</style>
