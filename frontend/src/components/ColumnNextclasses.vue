<template>
    <div class="nextclasses-column">
      <h2>{{ title }}</h2>
      <ul>
        <li v-for="(item, index) in nextClasses" :key="item.id">
          <div class="date-indicator" v-if="isFirstClassOfDay(nextClasses, index)">
            {{ formatDate(item.start) }}
          </div>
          <div :style="getEventStyle(item)" class="event-item" @click="goToClass(item.id)">
            <div class="event-header">
                <div class="event-start-time">{{ formatEventTime(item) }}</div>
                <div class="event-room">Room {{ item.room }}</div>
            </div>
            <div class="event-content">{{ item.text }}</div>
        </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    props: {
      title: {
        type: String,
        required: true
      },
    },
    data () {
      return {
        nextClasses: [],
        classesToDisplay: 20,
      };
    },
    async mounted () {
      const allClasses = await axios.get('http://127.0.0.1:5000/lessons', { withCredentials: true });
      const currentTime = new Date();
      this.nextClasses = allClasses.data.filter((course) => new Date(course.start) > currentTime).slice(0, this.classesToDisplay).map(course => ({
        id: course.id,
        text: course.title,  
        start: course.start,
        end: course.end,
        room: course.room,
        color: course.color,
      }));
      console.log(this.nextClasses);
    },
    methods: {
      goToClass(classId) {
        this.$router.push(`/class/${classId}`);
      },
      getEventStyle(item) {
        return {
          backgroundColor: item.color || '#4868bf' // Si la couleur n'est pas fournie, utilise une couleur par défaut (#4868bf)
        };
      },
      formatEventTime(item) {
        // Format de l'heure au format 'HH:mm'
        const eventTime = new Date(item.start);
        return eventTime.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
      },
      isFirstClassOfDay(list, index) {
        // Vérifie si c'est le premier cours de la journée en comparant les dates
        if (index === 0) {
          return true;
        } else {
          const currentStartTime = new Date(list[index].start).setHours(0, 0, 0, 0);
          const previousStartTime = new Date(list[index - 1].start).setHours(0, 0, 0, 0);
          return currentStartTime !== previousStartTime;
        }
      },
      formatDate(date) {
        // Format de la date au format 'dd/mm/yyyy'
        const eventDate = new Date(date);
        const options = { weekday: 'long', month: 'long', day: 'numeric' };
        return eventDate.toLocaleDateString('en-US', options);
      },
    }
  };
  </script>
  
  <style scoped>
  .nextclasses-column {
    flex: 1.5;
    padding: 20px;
    background-color: var(--secondary-color);
    color: var(--primary-text-color);
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    margin: 0 10px;
    overflow-y: auto;
  }
  
  h2 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    border-bottom: 1px solid #b0b0b0;
    padding-bottom: 10px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  
  .event-item {
    display: flex;
    flex-direction: column; /* Stack children vertically */
    padding: 10px;
    border-radius: 10px;
    color: white;
    margin-top: 10px;
    cursor: pointer;
}

.event-header {
    display: flex;
    justify-content: space-between; /* Pushes start time and room to opposite ends */
    width: 100%;
    font-size: 0.7rem
}

.event-start-time, .event-room {
    margin: 0; /* Remove any default margins for consistency */
}

.event-content {
    margin-top: 10px;
    font-size: 0.8rem;
}

  
  .date-indicator {
    display: flex;
    align-items: center;
    padding: 0;
    font-size: 0.8rem;
    position: relative;
    margin-top: 12px;
    margin-bottom: -5px;
    background-color: transparent;
}

.date-indicator::after {
    content: "";
    flex-grow: 1; /* allows the line to take up remaining space */
    height: 1px;
    background-color: #b0b0b0; /* color of the line */
    margin-left: 10px; /* space between the date and the line */
}
  </style>
  