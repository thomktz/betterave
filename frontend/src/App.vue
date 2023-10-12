<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  background: #a3cdcf;
  min-width: 100vh;
}

body, button, input, textarea {
  font-family: 'Montserrat', sans-serif;
}

.fc .fc-timegrid-col.fc-day-today {
    --fc-today-bg-color: #9ad2d28e; /* Color of the current day in the calendar */
}
</style>
