<template>
    <div>
      <FullCalendar :options="calendarOptions" />
    </div>
  </template>
  
  <script>
import { apiClient } from '@/apiConfig';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction';

  export default {
    name: 'UserCalendar',
    components: {
      FullCalendar
    },
    props: {
      user: {
        type: Object,
        required: true
      },
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
            const class_id = info.event.extendedProps.class_id;
            this.$router.push(`/class/${class_id}`);
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
        const lessonsResponse = await apiClient.get(`/users/me/lessons`);
        const eventsResponse = await apiClient.get(`/users/me/events`);

        this.calendarOptions.events = [...lessonsResponse.data, ...eventsResponse.data];
      } catch (error) {
        console.error("There was an error fetching lessons and events:", error);
      }
    },
    methods : {
    }
  }
  </script>
  
<style scoped>
div {
width: 100%;
background-color: var(--secondary-color);
color: var(--primary-text-color);
}
</style>