<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  mounted() {
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    document.documentElement.setAttribute("data-dark-mode", isDarkMode);
  },
};
</script>

<style>
/* Light Theme */
:root {
  --background-color: #a3cdcf;
  --foreground-color: #f5f5f5;
  --secondary-color: #f5f5f5;
  --primary-text-color: #000;
  --secondary-text-color: #5f5f5f;
  --text-bubble-color: #cdcdcd;
  /* Replicate the Vuetify colors */
  --v-input-border-color: rgba(50, 50, 50, 0.5);
  --v-input-background-color: rgba(50, 50, 50, 0.05);
  --v-input-text-color: rgba(20, 20, 20, 0.65);
}

/* Dark Theme */
[data-dark-mode="true"] {
  --background-color: #3d7276;
  --foreground-color: #2a2a2a;
  --secondary-color: #444444;
  --primary-text-color: #f5f5f5;
  --secondary-text-color: #bbbbbb;
  --text-bubble-color: #353535;
  /* Replicate the Vuetify colors */
  --v-input-border-color: rgba(200, 200, 200, 0.5);
  --v-input-background-color: rgba(245, 245, 245, 0.05);
  --v-input-text-color: rgba(245, 245, 245, 0.65);
}

/* General styles applicable to the entire app */
#app {
  background: var(--background-color);
  min-width: 100vh;
}

body,
button,
input,
textarea {
  font-family: "Montserrat", sans-serif;
  color: var(--primary-text-color);
}

.fc {
  --fc-today-bg-color: #9ad2d28e; /* Color of the current day in the calendar */
  --fc-border-color: #848484;
}
</style>
