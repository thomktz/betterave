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
            <router-link :to="'/student-details/' + student.id"> <!-- Note the use of :to to bind a dynamic route -->
    <img :src="student.profile_pic" :alt="student.name" />
    <p>{{ student.name }} {{ student.surname }}</p>
  </router-link>
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
        const response = await axios.get('/photochart', { withCredentials: true });
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
  padding: 20px;
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
  align-content: flex-start;
  padding-bottom: 30px; 
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
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.student {
  text-align: center;
  border: 1px solid #e0e0e0;
  border-radius: 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  padding: 0;  /* No padding so the image can take up the full space */
  position: relative;  /* Set to relative so absolute positioning of children is based on this container */
  overflow: hidden;  /* Keep the image and gradient inside the box */
}

.student::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;  /* This determines the height of the gradient, adjust if necessary */
  background: linear-gradient(transparent, rgba(0, 0, 0, 1));
  pointer-events: none; 
}

.student:hover img {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s, box-shadow 0.3s;
}

.student:hover::after {
  opacity: 0;  /* fade out gradient */
}

.student:hover p {
  opacity: 0;  /* fade out name */
}

.student::after, .student p {
  transition: opacity 0.3s;
}

img {
  width: 100%;  /* Full width of parent */
  height: 100%;  /* Full height of parent */
  object-fit: cover;
  display: block;  /* Remove any unwanted space below the image */
  transition: transform 0.3s, box-shadow 0.3s;
}

p {
  position: absolute;  /* Position it on top of the gradient */
  bottom: 10px;  /* From the bottom of the .student container */
  left: 50%;
  transform: translateX(-50%);  /* Center it horizontally */
  margin: 0;  /* Remove default margins */
  color: #fff;
  font-weight: bold;  /* Optional: Make the name stand out more */
  z-index: 2;
}
  </style>
    