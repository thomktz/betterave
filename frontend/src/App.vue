<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  mounted() {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    document.documentElement.setAttribute('data-dark-mode', isDarkMode);
  }
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
}

/* Dark Theme */
[data-dark-mode="true"] {
  --background-color: #3d7276;
  --foreground-color: #2a2a2a;
  --secondary-color: #444444;
  --primary-text-color: #f5f5f5;
  --secondary-text-color: #bbbbbb;
  --text-bubble-color: #353535;
}

/* General styles applicable to the entire app */
#app {
  background: var(--background-color);
  min-width: 100vh;
}

body, button, input, textarea {
  font-family: 'Montserrat', sans-serif;
  color: var(--primary-text-color);
}

.fc {
  --fc-today-bg-color: #9ad2d28e; /* Color of the current day in the calendar */
  --fc-border-color: #848484;
}

</style>
