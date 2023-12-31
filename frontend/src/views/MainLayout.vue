<template>
  <div>
    <header class="header">
      <div class="logos-block">
        <!-- Betterave Logo with Link to Home page -->
        <router-link to="/">
          <img
            src="/betterave-logo.png"
            alt="Betterave Logo"
            class="betterave-logo"
            title="Home page"
          />
        </router-link>

        <!-- ENSAE Logo with Link to ENSAE website -->
        <a
          href="https://www.ensae.fr/"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img
            src="/logo_ensae.png"
            alt="ENSAE Logo"
            class="ensae-logo"
            title="ENSAE website"
          />
        </a>
      </div>

      <h1>{{ headerTitle }}</h1>

      <div class="right-section">
        <ProfilePill :user="user" />
        <DarkModeToggle @toggle="toggleDarkMode" :darkMode="darkMode" />
      </div>
    </header>
    <router-view @updateTitle="setTitle" />
  </div>
</template>

<script>
import { apiClient } from "@/apiConfig";
import { ref } from "vue";
import ProfilePill from "@/components/ProfilePill.vue";
import DarkModeToggle from "@/components/DarkModeToggle.vue";

export default {
  components: {
    ProfilePill,
    DarkModeToggle,
  },
  data() {
    return {
      user: {},
      headerTitle: ref("Welcome to Betterave!"),
      darkMode: false,
    };
  },
  async mounted() {
    // Handle dark mode
    const storedPreference = localStorage.getItem("darkMode");
    if (storedPreference !== null) {
      this.darkMode = storedPreference === "true";
    } else {
      this.darkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
    }
    document.documentElement.setAttribute("data-dark-mode", this.darkMode);
    this.$vuetify.theme.name = this.darkMode ? "dark" : "light";
    try {
      const response = await apiClient.get("/users/me");
      this.user = response.data;
    } catch (error) {
      console.error("There was an error fetching user data:", error);
    }
  },
  methods: {
    setTitle(newTitle) {
      this.headerTitle = newTitle;
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      document.documentElement.setAttribute("data-dark-mode", this.darkMode);
      localStorage.setItem("darkMode", this.darkMode);

      // Update the Vuetify theme
      this.$vuetify.theme.name = this.darkMode ? "dark" : "light";
    },
  },
};
</script>

<style>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  background-color: var(--foreground-color-transparent);
  border-bottom: 1px solid var(--separator-color);
  z-index: 20;
  position: relative;
  opacity: 1;
}

.betterave-logo {
  height: 70px;
  width: auto;
  margin-left: 15px;
}

.ensae-logo {
  height: 120px;
  width: auto;
  margin-bottom: -20px;
}

.logos-block {
  display: flex;
  align-items: center;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-right: 20px;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
}

.fill-height {
  min-height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
</style>
