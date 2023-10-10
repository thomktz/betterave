<template>
  <v-container class="fill-height" fluid>
    <header class="header">
      <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />
      <h1>Hello, {{ user.name }}</h1>
      <ProfilePill :userEmail="user.email" @logout="logout" />
    </header>

    <div class="calendar-container">
      <StudentCalendar />
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
  align-items: center;
  justify-content: center;
  width: 100%;
}
</style>
