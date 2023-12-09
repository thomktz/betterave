<template>
    <div class="nextclasses-column">
      <h2>{{ title }}</h2>
      <ul>
        <li v-for="(item, index) in nextLessons" :key="item.id">
          <div class="date-indicator" v-if="isFirstClassOfDay(nextLessons, index)">
            {{ formatDate(item.start) }}
          </div>
          <div :style="getEventStyle(item)" class="event-item" @click="goToClass(item.class_id)">
            <div class="event-header">
                <div class="event-start-time">{{ formatEventTime(item) }}</div>
                <div class="event-room">Room {{ item.room }}</div>
            </div>
          <div class="event-content">{{ item.title }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { apiClient } from '@/apiConfig';

const limit = 50; 

export default {
  props: {
    user: {
      type: Object,
      required: true
    },
    title: {
      type: String,
      required: true
    },
  },
  data () {
    return {
      nextLessons: [],
      classesToDisplay: 20,
    };
  },
  async mounted () {
    // Get lessons
    const response = await apiClient.get('/users/me/lessons/future', { params: {limit: limit} });
    this.nextLessons = response.data;
  },
  methods: {
    goToClass(class_id) {
      this.$router.push(`/class/${class_id}`);
    },
    getEventStyle(item) {
      return {
        backgroundColor: item.backgroundColor || '#4868bf' // Default color
      };
    },
    formatEventTime(item) {
      // 'HH:mm' format
      const eventTime = new Date(item.start);
      return eventTime.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    },
    isFirstClassOfDay(list, index) {
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
  flex-direction: column;
  padding: 10px;
  border-radius: 10px;
  color: rgb(0, 0, 0);
  margin-top: 10px;
  cursor: pointer;
}

.event-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  font-size: 0.7rem
}

.event-start-time, .event-room {
  margin: 0;
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
    flex-grow: 1;
    height: 1px;
    background-color: #b0b0b0;
    margin-left: 10px;
}
  </style>