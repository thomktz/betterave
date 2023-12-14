<template>
  <div>
    <!-- Displaying the list of homework -->
    <ul>
      <li v-for="homework in homework" :key="homework.homework_id">
        {{ homework.content }} - {{ homework.due_date }} {{ homework.due_time }}
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
      required: true,
    },
  },
  data() {
    return {
      homework: [],
    };
  },
  async mounted() {
    // API call to get the list of homework
    try {
      const response = await apiClient.get(
        `/classes/${this.class_id}/homework`,
      );
      this.homework = response.data;
    } catch (error) {
      console.error("Error fetching homework:", error);
    }
  },
};
</script>
