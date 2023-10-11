<template>
  <v-container class="fill-height" fluid>
    <header class="header">
      <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />
      <h1>Hello, {{ user.name }}</h1>
      <ProfilePill :userEmail="user.email" />
    </header>

    <div class="content-container">
      <!-- Left Side Columns -->
      <div class="columns-container">
        <InfoColumn title="Next classes" :list="upcomingClasses" />
        <InfoColumn title="Homework" :list="homeworkList" />
        <InfoColumn title="Notifications" :list="notifications" />
      </div>

      <!-- Right Side Calendar -->
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
import InfoColumn from '@/components/InfoColumn.vue';

export default {
  components: {
    StudentCalendar,
    ProfilePill,
    InfoColumn,
  },
  data() {
    return {
      user: {
        name: '',
        email: ''
      },
      upcomingClasses: [{ id: 1, text: "Math class" , color: "#FF5733" }, { id: 2, text: "History class" }],
      homeworkList: [{ id: 1, text: "Algebra homework" }, { id: 2, text: "Essay on WW2" }],
      notifications: [{ id: 1, text: "Meeting tomorrow" }, { id: 2, text: "Homework due" }]
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
  width: 97%;
  padding: 15px; /* Padding to give space inside the square */
  background-color: #f5f5f5; /* Background color for the square */
  border-radius: 10px; /* Rounded corners */
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* subtle shadow for modern effect */
  margin-bottom: 20px; /* some margin to separate header from content */
}

.logo {
  height: 150px;
  width: auto;
}

h1 {
  font-size: 2rem;
  font-weight: 700; 
}

.calendar-box {
  background-color: #f5f5f5; /* light background color */
  border-radius: 10px; /* rounded corners */
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* subtle shadow for modern effect */
  width: calc(50% - 40px); /* adjust for padding */
  overflow: hidden; /* hide overflow for nested elements to ensure corners are rounded */
  height: 70vh;
}

.content-container {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  width: 100%;
}

.columns-container {
  display: flex;
  justify-content: space-between;
  width: calc(50% - 40px); /* adjust for padding */
  height: 70vh;
}

</style>
