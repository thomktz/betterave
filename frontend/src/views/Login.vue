<template>
  <v-container class="fill-height" fluid>
    <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />

    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12" dark>
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-text-field label="Email" name="login" prepend-icon="mdi-email" type="text"></v-text-field>
            <v-text-field label="Password" name="password" prepend-icon="mdi-lock" type="password"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    login() {
      // Handle your login logic here
    }
  }
};
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
  height: 250px;  /* Adjust as needed for your logo's dimensions */
  width: auto;
}
</style>