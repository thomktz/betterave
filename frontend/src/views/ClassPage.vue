<template>
    <v-container class="fill-height" fluid>
      <div class="content-section">
        <!-- Left Container -->
        <div class="info-container">
          <div class="class-header">
            <h1>Class details</h1>
          </div>
          <p><strong>ECTS Credits:</strong> {{ classDetails.ects_credits }}</p>
          <p><strong>Tutor:</strong> {{ classDetails.teacher }}</p>
          <p><a :href="classDetails.ensae_link" target="_blank">View ENSAE Link</a></p>
          <!-- Other information related to class -->
        </div>
    
        <!-- Middle Container -->
        <div class="info-container">
          <!-- Content for the middle container -->
        </div>
    
        <!-- Right Container -->
        <div class="info-container">
            <Chat :classId="classId" :userId="userId"></Chat>
        </div>
      </div>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  import Chat from '@/components/Chat.vue';
  
  export default {
    components: {
        Chat
    },
    data() {
      return {
        classDetails: {},
        classId: this.$route.params.classId,
        userId: NaN,
        userAuthorised: false
      };
    },
    async mounted() {
      const classId = this.$route.params.classId;
      try {
        const response = await axios.get(`/class/${classId}`, { withCredentials: true });
        this.classDetails = response.data;
        this.userId = this.classDetails.user_id;
        this.userAuthorised = this.classDetails.user_authorised;
        this.$emit('updateTitle', this.classDetails.name);
      } catch (error) {
        console.error("Error fetching class details:", error);
      }
    }
  }
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
  </style>
  