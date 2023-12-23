<template>
  <v-spacer class="trombi-grid" fluid>
    <div class="custom-select">
      <select v-model="selectedClass">
        <option value="all">Toutes les classes</option>
        <option v-for="cls in classes" :value="cls">{{ cls }}</option>
      </select>
    </div>

    <div class="trombinoscope">
      <div
        v-for="student in filteredStudents"
        :key="student.id"
        class="student"
      >
        <img :src="student.profile_pic" :alt="student.name" />
        <p>{{ student.name }} {{ student.surname }}</p>
      </div>
    </div>
  </v-spacer>
</template>

<script>
import { apiClient } from "@/apiConfig";

export default {
  data() {
    return {
      students: [],
      classes: ["1A", "2A", "3A"], // List of classes
      selectedClass: "all", // Current selected class
    };
  },
  computed: {
    filteredStudents() {
      if (this.selectedClass === "all") {
        return this.students;
      } else {
        return this.students.filter(
          (student) => student.level === this.selectedClass,
        );
      }
    },
  },
  async mounted() {
    this.$emit("updateTitle", "Trombinoscope"); // Update the title in the header
    try {
      const response = await apiClient.get("/users");
      this.students = response.data;
    } catch (error) {
      console.error("There was an error fetching student data:", error);
    }
  },
  methods: {},
};
</script>

<style scoped>
.trombi-grid {
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 100px);
  padding: 20px;
}

.custom-select {
  margin-top: 20px;
  margin-bottom: 20px;
  width: 250px;
  position: relative;
}

.trombinoscope {
  flex: 1;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  grid-auto-rows: 250px;
  gap: 20px;
  align-content: flex-start;
  padding-bottom: 30px;
}

.custom-select::after {
  content: "▼";
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  pointer-events: none;
}

.custom-select select {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--separator-color);
  border-radius: 5px;
  appearance: none;
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.student {
  text-align: center;
  border: 1px solid var(--separator-color);
  border-radius: 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.student::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(transparent, rgba(0, 0, 0, 1));
  pointer-events: none;
}

.student:hover img {
  transform: scale(1.1);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}

.student:hover::after {
  opacity: 0;
}

.student:hover p {
  opacity: 0;
}

.student::after,
.student p {
  transition: opacity 0.3s;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}

p {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  color: #fff;
  font-weight: bold;
  z-index: 2;
}
</style>
