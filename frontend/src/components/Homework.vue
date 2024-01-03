<template>
  <div class="homework-container">
    <ul>
      <li v-if="homework.length === 0" class="homework-item">
        No homework yet.
      </li>
      <li
        v-for="hw in homework"
        :key="hw.homework_id"
        :class="['homework-item', { 'past-due': isPastDue(hw.due_date) }]"
      >
        <div class="homework-header">
          <span class="homework-class-name">{{ hw.class_name }}</span>
          <span
            :class="['homework-due', { 'past-due': isPastDue(hw.due_date) }]"
            >{{ formatDueDate(hw.due_date, hw.due_time) }}</span
          >
        </div>
        <div class="homework-content">{{ hw.content }}</div>
      </li>
    </ul>
  </div>
</template>

<script>
import { apiClient } from "@/apiConfig";

export default {
  props: {
    class_id: {
      type: Number,
      required: false,
    },
  },
  data() {
    return {
      homework: [],
    };
  },
  async mounted() {
    try {
      if (!this.class_id) {
        // If class_id is not provided, fetch all homework
        const response = await apiClient.get("/classes/homework");
        // Reverse the list
        response.data.reverse();
        this.homework = response.data;
      } else {
        // Otherwise, fetch homework for the specified class
        const response = await apiClient.get(
          `/classes/${this.class_id}/homework`,
        );
        // Reverse the list
        response.data.reverse();
        this.homework = response.data;
      }
    } catch (error) {
      console.error("Error fetching homework:", error);
    }
  },
  methods: {
    formatDueDate(date, time) {
      // Convert HH:MM:SS to HH:MM
      if (time) {
        time = time.slice(0, 5);
      }
      return `${date} ${time || ""}`.trim();
    },
    isPastDue(dueDate) {
      return new Date(dueDate) < new Date();
    },
  },
};
</script>

<style scoped>
.homework-container {
  position: relative;
  max-height: 65vh;
  overflow: auto;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.homework-item {
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-radius: 10px;
  background-color: #4868bf;
  color: #eee;
  margin-top: 10px;
}
.homework-item.past-due {
  background-color: rgb(222, 220, 220);
  color: #383535; /* Dark grey text for past homework */
}

.homework-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.homework-class-name {
  font-weight: bold;
}

.homework-due {
  font-style: italic;
  color: #eeeeeee4;
}
.homework-due.past-due {
  font-style: italic;
  color: #7e1111c6;
}

.homework-content {
  font-size: 0.8rem;
}
</style>
