<template>
  <v-container class="fill-height" fluid>
    <div class="content-container">
      <div class="class-list-container">
        <ul v-if="classes.length">
          <li v-for="classes" :key="classItem.class_id">
            <span class="class-name">{{ classItem.name }}</span>
          </li>
        </ul>
        <div v-else>Loading classes...</div>
      </div>
    </div>
  </v-container>
</template>

<script>
import { apiClient } from "@/apiConfig";

export default {
  data() {
    return {
      user_id: "me",
      classes: [],
    };
  },
  async mounted() {
    this.$emit("updateTitle", "Classes");
    try {
      const response = await apiClient.get(`/classes/teacherclasses/${this.user_id}`);
      this.classes = response.data;
    } catch (error) {
      console.error("Error fetching teacher classes:", error);
    }
  },
};
</script>

<style scoped>
.class-list-container {
  background-color: var(--foreground-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 70%;
  max-height: 70vh;
  overflow-y: auto;
  margin: auto;
}

.content-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
  width: 100%;
}

li {
  display: flex;
  align-items: center;
  height: 70px;
  border-bottom: 1px solid #b0b0b0;
  transition: background-color 0.2s ease;
}

li:hover {
  background-color: rgba(123, 123, 123, 0.4);
}

.class-name {
  flex-grow: 1;
}
</style>
