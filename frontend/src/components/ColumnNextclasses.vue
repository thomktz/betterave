<template>
    <div class="info-column">
      <h2>{{ title }}</h2>
      <ul>
        <li v-for="(item, index) in list" :key="item.id">
          <div class="event-item" :style="getEventStyle(item)">
            <div class="event-time">{{ formatEventTime(item) }}</div>
            <div class="event-text">{{ item.text }}</div>
          </div>
          <!-- Ajout d'une ligne pour afficher la date si c'est le premier cours de la journée -->
          <div v-if="isFirstClassOfDay(list, index)" class="date-indicator">
            {{ formatDate(item.start) }}
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: {
        type: String,
        required: true
      },
      list: {
        type: Array,
        default: () => []
      }
    },
    methods: {
      getEventStyle(item) {
        return {
          backgroundColor: item.color || '#4868bf'
        };
      },
      formatEventTime(item) {
        // Format de l'heure au format 'HH:mm'
        return new Date(item.start).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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
        return new Date(date).toLocaleDateString();
      }
    }
  };
  </script>
  
  <style scoped>
  .info-column {
    flex: 1;
    padding: 20px;
    background-color: white;
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    margin: 0 10px;
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
    padding: 10px;
    border-radius: 10px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .event-time {
    font-size: 0.8rem; /* Texte plus petit pour l'heure */
  }
  
  .date-indicator {
    text-align: center;
    background-color: #f5f5f5;
    padding: 5px;
    border-radius: 5px;
    margin-top: 10px;
  }
  </style>
  