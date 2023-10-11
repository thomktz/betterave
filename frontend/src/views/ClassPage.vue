<template>
    <v-container class="fill-height" fluid>
      <div class="content-section">
        <!-- Left Container -->
        <div class="info-container">
          <div class="class-header">
            <h1>{{ classDetails.name }}</h1>
          </div>
          <p><strong>ECTS Credits:</strong> {{ classDetails.ects_credits }}</p>
          <p><strong>Tutor:</strong> {{ classDetails.tutor }}</p>
          <p><a :href="classDetails.ensae_link" target="_blank">View ENSAE Link</a></p>
          <!-- Other information related to class -->
        </div>
    
        <!-- Middle Container -->
        <div class="info-container">
          <!-- Content for the middle container -->
        </div>
    
        <!-- Right Container -->
        <div class="info-container">
          <!-- Content for the right container -->
        </div>
      </div>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        classDetails: {}
      };
    },
    async mounted() {
      const classId = this.$route.params.classId;
      try {
        const response = await axios.get(`http://127.0.0.1:5000/class/${classId}`, { withCredentials: true });
        this.classDetails = response.data;
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
    background-color: #f5f5f5;
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    width: calc(33.333% - 30px); /* Adjusting for the space between containers */
    padding: 20px;
    height: 70vh; /* Adjust based on your design preference */
  }
  
  .class-header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 20px; /* space between title and content */
  }
  </style>
  