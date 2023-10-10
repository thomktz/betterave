<template>
  <v-container class="fill-height" fluid>
    <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />

    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" dark>
          <v-card-title>Welcome, {{ user.name }}</v-card-title>
          <v-card-text>
            <p>Email: {{ user.email }}</p>
            <!-- Add more fields as needed -->
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="logout">Logout</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
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
    async logout() {
      try {
        await axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true });
        // Redirect to Login page
        this.$router.push({ name: 'Login' });
      } catch (error) {
        console.error("There was an error logging out:", error);
      }
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: #a3cdcf;
}

.logo {
  position: absolute;
  top: 20px;
  left: 20px;
  height: 250px;
  width: auto;
}
</style>
