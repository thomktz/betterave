<template>
  <v-spacer class="trombi-grid" fluid>
    <div class="custom-select">
      <select v-model="selectedClass">
        <option value="all">Toutes les classes</option>
        <option v-for="cls in classes" :value="cls">{{ cls }}</option>
      </select>
    </div>

    <div class="trombinoscope">
      <div v-for="student in filteredStudents" :key="student.id" class="student">
        <img :src="student.profile_pic" :alt="student.name" />
        <p>{{ student.name }} {{ student.surname }}</p>
      </div>
    </div>
    </v-spacer>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        students: [],
        classes: ['1A', '2A', '3A'], // List of classes
        selectedClass: 'all', // Current selected class
    };
},
    computed: {
      filteredStudents() {
        if (this.selectedClass === 'all') {
          return this.students;
        } else {
          return this.students.filter((student) => student.level === this.selectedClass);
        }
      },
    },
    async mounted() {
      this.$emit('updateTitle', "Trombinoscope"); // Update the title in the header
      try {
        const response = await axios.get('http://127.0.0.1:5000/photochart', { withCredentials: true });
        this.students = response.data;
      } catch (error) {
        console.error("There was an error fetching student data:", error);
      }
    },
    methods: { },
  }

  
  </script>
  
  <style scoped>
.trombi-grid {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 150px);
}

.custom-select {
  margin-top: 20px;
  margin-bottom: 20px;
  width: 250px;
  position: relative;
}

/* Styles for the trombinoscope to occupy the remaining height after .custom-select */
.trombinoscope {
  flex: 1; 
  overflow-y: auto; 
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  grid-auto-rows: 250px; /* Set fixed row height */
  gap: 20px;
  align-content: flex-start; /* Prevents grid items from stretching if there are only a few rows */
}

.custom-select::after { 
  content: '▼'; 
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  pointer-events: none;
}

.custom-select select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  appearance: none;
  background-color: #f2f2f2;
  color: #333;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.student {
  text-align: center;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  padding: 10px;
  overflow: hidden;
}
img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 50%;
  margin-top: 10px;
}

  </style>
    