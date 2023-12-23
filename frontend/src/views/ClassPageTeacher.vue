<template>
  <div class="fill-height" fluid>
    <div class="content-section">
      <!-- Left Container -->
      <div class="info-container">
        <div class="class-header">
          <h1>Class details</h1>
        </div>
        <p><strong>ECTS Credits:</strong> {{ classDetails.ects_credits }}</p>
        <p><strong>Tutor:</strong> {{ classDetails.teacher }}</p>
        <p>
          <a :href="classDetails.ensae_link" target="_blank">View ENSAE Link</a>
        </p>
        <!-- Container for "Edit Grades" text and pencil icon -->
        <div class="edit-container" @click="redirectToEditGrades">
          <span><h1>Edit Grades</h1></span>
          <v-icon class="edit-icon">mdi-pencil</v-icon>
        </div>
        <!-- Other information related to class -->
      </div>

      <!-- Middle Container -->
      <div class="info-container">
        <div class="class-header">
          <h1>Homework</h1>
        </div>
        <Homework :class_id="class_id"></Homework>
      </div>

      <!-- Right Container -->
      <div class="info-container">
        <Chat :class_id="class_id" :user_id="user_id"></Chat>
      </div>
    </div>
  </div>
</template>

<script>
import Chat from "@/components/Chat.vue";
import { apiClient } from "@/apiConfig";
import Homework from "@/components/Homework.vue";

export default {
  components: {
    Homework,
    Chat,
  },
  data() {
    return {
      classDetails: {},
      class_id: parseInt(this.$route.params.class_id),
      user_id: NaN,
      newHomework: {
        content: "",
        due_date: null,
      },
    };
  },
  async mounted() {
    try {
      const response = await apiClient.get(`/classes/${this.class_id}`);
      this.classDetails = response.data;
      this.$emit("updateTitle", this.classDetails.name + " Professor page");
    } catch (error) {
      console.error("Error fetching class details:", error);
    }
    try {
      const response = await apiClient.get("/users/me");
      this.user_id = response.data.user_id;
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  },
  methods: {
    redirectToEditGrades() {
      // Programmatically navigate to the 'edit-grades' route
      this.$router.push(`/class/${this.class_id}/prof/grades`);
    },
  },
};
</script>

<style scoped>
.content-section {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 20px;
}

.info-container {
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  width: calc(33.333% - 30px); /* Adjusting for the space between containers */
  padding: 20px;
  height: 70vh;
}

.class-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 20px; /* space between title and content */
}

.edit-container {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.edit-container span {
  margin-right: 10px;
}

.edit-icon {
  font-size: 2rem;
}
</style>
