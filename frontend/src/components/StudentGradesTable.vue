<template>
  <v-container class="main-container">
    <v-container class="inner-container">
      <v-row align="stretch" class="row">
      </v-row>

      <!-- Classes Table -->
      <v-data-table
        :headers="headers"
        :items="classes"
        class="actual-table"
        dense>
        
        <!-- Class Name Column -->
        <template v-slot:[`item.class_name`]="{ item }">
          <span class="cell-height cell-width">{{ item.class_name }}</span>
        </template>

        <!-- ECTS Column -->
        <template v-slot:[`item.class_ects`]="{ item }">
          <span class="cell-height cell-width">{{ item.class_ects }}</span>
        </template>

        <!-- Grades Column -->
        <template v-slot:[`item.gradesByClassId`]="{ item }">
          <span class="cell-height cell-width">
            {{ formatGrades(item.gradesByClassId) }}
          </span>
        </template>
      </v-data-table>
    </v-container>
  </v-container>
</template>

<script>
export default {
  props: {
    classes: Array,
    asAdmin: Boolean,
  },
  data() {
    return {
      headers: [
        { title: "Class Name", value: "class_name", width: "150" },
        { title: "ECTS", value: "class_ects", width: "100" },
        { title: "Secondary Group", value: "secondary_class_group_name", width: "200" },
        { title: "Grades", value: "grade", width: "100" },
      ],
    };
  },
  methods: {
    formatGrades(grades) {
  console.log("Grades in formatGrades:", grades);

  if (!grades || !Array.isArray(grades)) {
    return '';
  }

  // Assumption: Each grade has a "grade" property
  return grades.map(grade => `${grade.grade}`).join(', ');
},
  },
  computed: {
    totalECTS() {
      return this.classes.reduce((total, classItem) => total + classItem.class_ects, 0);
    },
    ectsColor() {
      const total = this.totalECTS;
      return total >= 30 && total <= 32 ? "green" : "red";
    },
  },
};
</script>

<style scoped>
/* Styles spécifiques au composant */
.main-container {
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  padding: 16px;
  margin-top: 20px;
  border-radius: 15px;
}

.inner-container {
  border-radius: 5px;
  padding: 0;
}

.actual-table {
  max-width: 1300px;
  position: relative;
  z-index: 1;
}

.ects-counter {
  display: flex;
  align-items: center;
  margin-right: 20px;
  justify-content: flex-start;
}

.ects-text {
  margin-right: 8px;
}

.ects-value {
  margin-right: 8px;
}

.row {
  padding: 10px;
  margin-left: 20px;
}

.info-icon {
  cursor: pointer;
}

.icon-btn {
  background-color: var(--secondary-color);
}

.cell-width {
  width: 200px;
}

.cell-height {
  height: 40px;
}
</style>
