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
          events: [],
          slotMinTime: '08:00:00',
          slotMaxTime: '20:00:00',
          hiddenDays: [0, 6],
          height: '90vh'
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
  div {
  width: 100%;
  }
</style>
  