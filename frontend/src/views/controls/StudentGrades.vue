<template>
  <v-container class="fill-height">
    <!-- Recap -->
    <v-container class="summary-container">
      <v-row>
        <v-col class="summary-box">
          <div class="summary-title">Total ECTS</div>
          <div class="summary-value">{{ totalECTS }}</div>
        </v-col>
        <v-col class="summary-box">
          <div class="summary-title">Average Grade</div>
          <div class="summary-value">{{ averageGrade.toFixed(2) }}</div>
        </v-col>
      </v-row>
    </v-container>

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
          <tr
            v-for="(item, index) in allGrades"
            :key="index"
            @click="goToClass(item.class_id)"
            class="clickable-row"
          >
            <td>{{ item.class_name }}</td>
            <td class="text-center">{{ item.class_ects }}</td>
            <td class="text-center">
              {{ item.grades[0] ? item.grades[0].grade : "-" }}
            </td>
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
      allGrades: [],
    };
  },
  async mounted() {
    try {
      const response = await apiClient.get(
        `/users/${this.user_id}/classgroups`,
      );
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
  computed: {
    totalECTS() {
      return this.allGrades.reduce((total, item) => total + item.class_ects, 0);
    },
    averageGrade() {
      let totalGradedECTS = 0;
      const weightedSum = this.allGrades.reduce((sum, item) => {
        if (item.grades[0]) {
          totalGradedECTS += item.class_ects;
          return sum + item.grades[0].grade * item.class_ects;
        }
        return sum;
      }, 0);

      return totalGradedECTS > 0 ? weightedSum / totalGradedECTS : 0;
    },
  },
  methods: {
    async fetchGradesForClasses() {
      try {
        for (const enrolledClass of this.classes) {
          const classId = enrolledClass.class_id;
          const response = await apiClient.get(
            `/users/${classId}/grades/${this.user_id}`,
          );
          const grades = response.data;

          this.allGrades.push({
            class_name: enrolledClass.class_name,
            class_ects: enrolledClass.class_ects,
            class_id: classId,
            grades: grades,
          });
        }
      } catch (error) {
        console.error("Error fetching grades for classes:", error);
      }
    },
    goToClass(class_id) {
      this.$router.push(`/class/${class_id}`);
    },
  },
};
</script>

<style scoped>
.clickable-row {
  cursor: pointer;
}
.clickable-row:hover {
  background-color: rgba(122, 122, 122, 0.5) !important;
}
.fill-height {
  justify-content: center;
}
.grades-table {
  width: 800px;
  margin-top: 20px;
  border-collapse: collapse;
}
.grades-table th:first-child,
.grades-table td:first-child {
  width: 800px;
  white-space: nowrap;
}
.font-weight-bold {
  font-weight: bold;
}
.grades-table td,
.grades-table th {
  padding: 8px;
  border: 1px solid rgba(120, 120, 120, 0.602);
}
.grades-table tr,
th {
  background-color: var(--secondary-color) !important;
}
.summary-container {
  background-color: var(--secondary-color);
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 15px;
}

.summary-box {
  text-align: center;
  padding: 20px;
  background-color: var(--light-background-color);
  border-radius: 10px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.summary-title {
  font-size: 0.8em;
  color: var(--primary-text-color);
  margin-bottom: 10px;
}

.summary-value {
  font-size: 2.5em;
  font-weight: bold;
  color: var(--highlight-color);
}
</style>
