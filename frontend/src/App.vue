<template>
  <div class="image-overlay">
    <div class="image-container">
      <picture>
        <source srcset="/light_overlay.avif" type="image/avif" />
        <img src="/light_overlay_png.png" alt="" class="light-image" />
      </picture>
      <picture>
        <source srcset="/dark_overlay.avif" type="image/avif" />
        <img src="/light_overlay_png.png" alt="" class="dark-image" />
      </picture>
    </div>
  </div>
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
.image-overlay {
  position: absolute;
  z-index: 0;
  top: 0;
  left: 0;
  right: 0;
  overflow: hidden;
  pointer-events: none;
  display: flex;
  justify-content: center;
}

.image-container {
  flex: none;
  display: flex;
  justify-content: end;
}

/* Add these styles to manage the visibility of the images */
.light-image {
  width: auto;
  max-width: none;
  display: block;
}

.dark-image {
  width: auto;
  max-width: none;
  display: none;
}

/* Use the mounted attribute to toggle dark mode */
[data-dark-mode="true"] .light-image {
  display: none;
}

[data-dark-mode="true"] .dark-image {
  display: block;
}

/* Light Theme */
:root {
  --background-color: #e8e1e1;
  --foreground-color: #e8e1e1;
  --foreground-color-transparent: rgba(245, 245, 245, 0.4);
  --secondary-color: rgba(245, 245, 245, 0.4);
  --secondary-color-transparent: rgba(245, 245, 245, 0.4);
  --primary-text-color: #000;
  --secondary-text-color: #5f5f5f;
  --text-bubble-color: #cdcdcd;
  --separator-color: #b0b0b0;

  --v-input-border-color: rgba(50, 50, 50, 0.5);
  --v-input-background-color: rgba(50, 50, 50, 0.05);
  --v-input-text-color: rgba(20, 20, 20, 0.65);
}

/* Dark Theme */
[data-dark-mode="true"] {
  --background-color: rgb(15, 23, 42);
  --foreground-color: rgb(15, 23, 42);
  --foreground-color-transparent: rgba(15, 23, 42, 0.1);
  --secondary-color: rgb(30, 41, 59);
  --secondary-color-transparent: rgba(255, 255, 255, 0.05);
  --primary-text-color: #f5f5f5;
  --secondary-text-color: #bbbbbb;
  --text-bubble-color: #353535;
  --separator-color: rgb(248, 250, 252, 0.1);

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
  --fc-today-bg-color: #9ad2d28e;
  --fc-border-color: #848484;
}
.fc .fc-toolbar.fc-header-toolbar {
  margin: 0 !important;
  margin-bottom: 0 !important;
}
.fc .fc-toolbar-title {
  border-bottom: none !important;
  padding-bottom: 0 !important;
}
</style>
