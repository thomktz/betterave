<template>
  <v-container class="fill-height" fluid>
    <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />

    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" dark>
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-text-field label="Email" v-model="email" prepend-icon="mdi-email" type="text"></v-text-field>
            <v-text-field label="Password" v-model="password" prepend-icon="mdi-lock" type="password"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="login">Login</v-btn>
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
      email: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        });
        if (response.data.status === "success") {
          // Assume the token is returned in the response. Adjust the property path as needed.
          const token = response.data.token;
          
          // Save token to local storage (or session storage or cookies, based on preference)
          localStorage.setItem('authToken', token);
          
          // Redirect user to home page using Vue Router
          this.$router.push({ name: 'homepage' });
        } else {
          console.error("Login failed:", response.data.message);
        }
      } catch (error) {
        console.error("There was an error logging in:", error);
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