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
    name: 'UserCalendar',
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
          locale: 'fr',
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridDay,timeGridWeek,listWeek'
          },
          eventTextColor: '#000000',
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
    },
    methods : {
    }
  }
  </script>
  
<style scoped>
  div {
  width: 100%;
  }
  .tooltip .tooltip-inner {
  background-color: #fff;
  color: #333;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.tooltip .tooltip-arrow {
  border-color: #ccc;
}
</style>
  