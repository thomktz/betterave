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
          locale: 'fr',
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridDay,timeGridWeek,listWeek'
          },
          eventTextColor: '#000000',
          nowIndicator: true, 
          eventDidMount: function(info) {
            // Insert the room info after the times
            const timeTextNode = info.el.querySelector('.fc-event-time');
            if (timeTextNode) {
              const roomSpan = document.createElement('span');
              roomSpan.textContent = `${info.event.extendedProps.room}`;
              roomSpan.style.marginLeft = '30px';
              timeTextNode.appendChild(roomSpan);
            }
          },
          eventClick: (info) => {
            const classId = info.event.extendedProps.class_id;
            this.$router.push(`/class/${classId}`);
          },
          eventMouseEnter: function(info) {
            info.el.style.cursor = 'pointer';
          },
          eventMouseLeave: function(info) {
            info.el.style.cursor = '';
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
  