<template>
  <v-snackbar
    v-model="showSnackbar"
    color="error"
    :timeout="1000"
    right
    top 
  >
    Incorrect e-mail or password!
    <v-btn
        dark
        text
        @click="showSnackbar = false"
    >
        Close
    </v-btn>
</v-snackbar>
<v-container class="fill-height" fluid>
    <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />
    <v-row align="center" justify="center" style="width: 100%;">
      <v-col cols="12" sm="8" md="4" class="login-col">
        <img src="/betterave-logo.png" alt="Betterave Logo" class="betterave-logo" />
        <v-card class="elevation-12" dark>
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-text-field label="Email" v-model="email" prepend-icon="mdi-email" type="text"></v-text-field>
            <v-text-field label="Password" v-model="password" prepend-icon="mdi-lock" type="password" @keyup.enter="login"></v-text-field>
          </v-card-text>
          <v-card-actions class="login-button">
            <v-btn rounded block class="centered-button" @click="login">
              Login
            </v-btn>
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
      password: '',
      showSnackbar: false
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        }, 
        { 
          withCredentials: true
        });
        if (response.data.status === "success") {
          console.log("Login successful!");
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
.centered-button {
  background-color: #80808084;
  text-align: center;
  margin: 0 auto; 
  display: block; 
}
.betterave-logo {
  width: 70%;
  height: auto;
  margin-bottom: 10px; /* The only margin required is at the bottom to space it from the card */
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.login-button {
  padding: 0.5rem 2rem;
}

.centered-button {
    background: linear-gradient(90deg, #80808084 50%, #4CAF50 50%);
    background-size: 200% 100%;
    transition: background-position 0.5s ease;
}

.centered-button:hover {
    background-position: -100% 0;
}


.login-col {
  margin-bottom: 100px;
}
</style>