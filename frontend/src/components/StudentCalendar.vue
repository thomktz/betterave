<!-- LessonCalendar.vue -->

<template>
    <div>
      <FullCalendar :options="calendarOptions" />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import FullCalendar from '@fullcalendar/vue3'
  import timeGridPlugin from '@fullcalendar/timegrid';
  import interactionPlugin from '@fullcalendar/interaction';
  
  export default {
    name: 'StudentCalendar',
    components: {
      FullCalendar
    },
    data() {
      return {
        calendarOptions: {
          plugins: [ timeGridPlugin, interactionPlugin ],
          initialView: 'timeGridWeek',
          events: []
        },
      };
    },
    async mounted() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/lessons', { withCredentials: true });
        this.calendarOptions.events = response.data;
      } catch (error) {
        console.error("There was an error fetching lessons:", error);
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add styles here if necessary */
  </style>
  