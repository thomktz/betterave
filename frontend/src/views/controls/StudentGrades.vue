<template>
  <v-container class="main-container"> <!-- Ajout de la classe text-center pour centrer -->
    <!-- Grades Table -->
    <v-simple-table class="grades-table mx-auto" dense>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="font-weight-bold text-left">Class Name</th>
            <th class="font-weight-bold text-center">ECTS</th>
            <th class="font-weight-bold text-center">Grade</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in allGrades" :key="index">
            <td>{{ item.class_name }}</td>
            <td class="text-center">{{ item.class_ects }}</td>
            <td class="text-center">{{ item.grades[0] ? item.grades[0].grade : 'No grade available' }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-container>
</template>
<script>
import { apiClient } from "@/apiConfig";

export default {
  data() {
    return {
      user_id: "me",
      classesInfo: {},
      classes: [],
      availableClasses: [],
      name: "",
      surname: "",
      level: null,
      allGrades: [], // New array to store all grades for display
    };
  },
  async mounted() {
    try {
      const response = await apiClient.get(`/users/${this.user_id}/classgroups`);
      this.classesInfo = response.data;
      this.classes = this.classesInfo.classgroups;
      this.name = this.classesInfo.name;
      this.surname = this.classesInfo.surname;
      this.level = this.classesInfo.level;

      this.$emit("updateTitle", `${this.name} ${this.surname} Grades`);

      await this.fetchGradesForClasses();
    } catch (error) {
      console.error("Error fetching classes:", error);
    }
  },
  methods: {
    async fetchGradesForClasses() {
      try {
        for (const enrolledClass of this.classes) {
          const classId = enrolledClass.class_id;
          const response = await apiClient.get(`/users/${classId}/gradesbis/${this.user_id}`);
          const grades = response.data;

          this.allGrades.push({
            class_name: enrolledClass.class_name,
            class_ects: enrolledClass.class_ects,
            grades: grades,
          });
        }
      } catch (error) {
        console.error("Error fetching grades for classes:", error);
      }
    },
  },
};
</script>

<style scoped>
.main-container {
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  padding: 40px;
  margin-top: 20px;
  border-radius: 15px;
}

.grades-table {
  width: 800px; /* Augmentation de la largeur */
  margin-top: 20px;
  border-collapse: collapse; /* Ajout pour afficher les bordures */
}

/* Augmentation de la largeur de la première colonne */.grades-table th:first-child,
.grades-table td:first-child {
  width: 800px; /* Ajustez la largeur de la première colonne selon vos besoins */
  white-space: nowrap; /* Empêche le retour à la ligne dans la première colonne */
}


.font-weight-bold {
  font-weight: bold;
}

.grades-table td,
.grades-table th {
  padding: 8px;
  border: 1px solid white; /* Remplacez 'white' par '#ffffff' si vous préférez utiliser la notation hexadécimale */
}

/* Ajout d'un fond coloré pour améliorer la visibilité des cellules */
.grades-table td {
  background-color: var(--secondary-color);
}
</style>
