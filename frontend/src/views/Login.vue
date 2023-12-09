<template>
  <v-container class="fill-height" fluid>
    <img src="/logo_ensae.png" alt="ENSAE Logo" class="logo" />
    <v-row align="center" justify="center" style="width: 100%">
      <v-col cols="12" sm="8" md="4" class="login-col">
        <img
          src="/betterave-logo.png"
          alt="Betterave Logo"
          class="betterave-logo"
        />
        <v-card class="elevation-12" dark>
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-text-field
              label="Email"
              v-model="email"
              prepend-icon="mdi-email"
              type="text"
              placeholder="john.doe@ensae.fr"
            ></v-text-field>
            <v-text-field
              label="Password"
              v-model="password"
              prepend-icon="mdi-lock"
              type="password"
              @keyup.enter="login"
            ></v-text-field>
          </v-card-text>
          <v-card-actions class="login-button">
            <v-btn rounded block class="centered-button" @click="login">
              Login
            </v-btn>
            <!-- Registration Link -->
          </v-card-actions>
          <v-card-text class="text-center">
            <a
              class="text-blue text-decoration-none"
              @click="openRegisterDialog"
            >
              Sign up now <v-icon icon="mdi-chevron-right"></v-icon>
            </a>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <RegisterDialog ref="registerDialog"></RegisterDialog>
  </v-container>
</template>
<script>
import { apiClient, toast } from "@/apiConfig";
import RegisterDialog from "@/components/RegisterDialog.vue";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  components: {
    RegisterDialog,
  },
  mounted() {
    this.logout();
  },
  methods: {
    openRegisterDialog() {
      if (this.$refs.registerDialog) {
        this.$refs.registerDialog.open();
      } else {
        console.error("RegisterDialog component not found");
      }
    },
    login() {
      apiClient
        .post("/auth/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          this.$router.push({ name: "homepage" });
        });
    },
    logout() {
      apiClient
        .post("/auth/logout")
        .then(() => {
          console.log("Logged out successfully.");
        })
        .catch((error) => {
          console.error("Error during logout: ", error);
        });
    },
  },
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
  margin-bottom: 10px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.v-card-text {
  padding-bottom: 0px;
}
.login-button {
  padding: 0.5rem 2rem;
}

.centered-button {
  background: linear-gradient(90deg, #80808084 50%, #4caf50 50%);
  background-size: 200% 100%;
  transition: background-position 0.5s ease;
}

.centered-button:hover {
  background-position: -100% 0;
}
.text-center {
  padding: 5px;
  cursor: pointer;
}

.login-col {
  margin-bottom: 100px;
}
</style>
