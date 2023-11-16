<template>
    <div>
      <!-- Displaying the list of homework -->
      <ul>
        <li v-for="homework in homeworks" :key="homework.homework_id">
          {{ homework.content }} - {{ formatDate(homework.due_date) }}
        </li>
      </ul>
  
      <!-- Form for adding a new homework -->
      <div>
        <textarea v-model="newHomeworkContent" placeholder="Enter the new homework"></textarea>
        <button @click="addHomework">Add Homework</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      group_id: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        homeworks: [],
        newHomeworkContent: "",
      };
    },
    methods: {
      // Method to add a new homework
      async addHomework() {
        try {
          // API call to add a new homework
          const response = await this.$api.post(`/classes/${this.group_id}/homeworks`, {
            content: this.newHomeworkContent,
          });
  
          // Update the homework list after adding
          this.homeworks.push(response.data);
          this.newHomeworkContent = ""; // Clear content after adding
        } catch (error) {
          console.error("Error adding homework:", error);
        }
      },
      // Other useful methods, e.g., for formatting the date
      formatDate(due_date) {
        // ...
      },
    },
    async mounted() {
      // API call to get the list of homework
      try {
        const response = await this.$api.get(`/classes/${this.group_id}/homeworks`);
        this.homeworks = response.data;
      } catch (error) {
        console.error("Error fetching homework:", error);
      }
    },
  };
  </script>
  