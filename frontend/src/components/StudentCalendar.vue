<!-- LessonCalendar.vue -->

<template>
    <div>
      <FullCalendar :options="calendarOptions" />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import FullCalendar from '@fullcalendar/vue3'
  import dayGridPlugin from '@fullcalendar/daygrid'; // for day view
  import timeGridPlugin from '@fullcalendar/timegrid'; // for week view
  import listPlugin from '@fullcalendar/list'; // for list view

  import interactionPlugin from '@fullcalendar/interaction';
  
  export default {
    name: 'StudentCalendar',
    components: {
      FullCalendar
    },
    data() {
      return {
        calendarOptions: {
          plugins: [ timeGridPlugin, interactionPlugin, dayGridPlugin, listPlugin ],
          initialView: 'timeGridWeek',
          events: [],
          slotMinTime: '08:00:00',
          slotMaxTime: '20:00:00',
          hiddenDays: [0, 6],
          height: '90vh',
          allDaySlot: false,
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridDay,timeGridWeek,listWeek'
          }
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
  