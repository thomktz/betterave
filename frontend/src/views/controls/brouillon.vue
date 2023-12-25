<template>
  <v-container class="fill-height">
    <StudentGradesTable
      :classes="classes"
      :available-classes.sync="availableClasses"
      @request-classes="fetchClasses"
      @enroll-class="enrollInClass"
      @update-class-group="updateClassGroup"
      @delete-class="deleteClass"
    />
  </v-container>
</template>

<script>
import { apiClient, toast } from "@/apiConfig";
import StudentGradesTable from "@/components/StudentGradesTable.vue";

export default {
  components: {
    StudentGradesTable,
  },
  data() {
    return {
      user_id: "me",
      classesInfo: {},
      classes: [],
      availableClasses: [],
      name: "",
      surname: "",
      level: null,
      gradesByClassId: {}, // New object to store grades by class_id
    };
  },
  async mounted() {
    // Fetch the classes for the selected user
    try {
      const response = await apiClient.get(`/users/${this.user_id}/classgroups`);
      this.classesInfo = response.data;
      this.classes = this.classesInfo.classgroups;
      this.name = this.classesInfo.name;
      this.surname = this.classesInfo.surname;
      this.level = this.classesInfo.level;

      this.$emit("updateTitle", `${this.name} ${this.surname} Grades`);

      // Fetch grades for each class and store them in gradesByClassId
      await this.fetchGradesForClasses();
    } catch (error) {
      console.error("Error fetching classes:", error);
    }
  },
  methods: {
    async fetchClasses() {
      try {
        const response = await apiClient.get(`/classes/level/${this.level}`);
        const allAvailableClasses = response.data;

        // Filter out classes that are already enrolled
        this.availableClasses = allAvailableClasses.filter(
          (availableClass) =>
            !this.classes.some(
              (enrolledClass) =>
                enrolledClass.class_id === availableClass.class_id,
            ),
        );
      } catch (error) {
        console.error("Error fetching classes:", error);
      }
    },
    async fetchGradesForClasses() {
  try {
    // Fetch grades for each class and store them in gradesByClassId
    for (const enrolledClass of this.classes) {
      const classId = enrolledClass.class_id;
      const response = await apiClient.get(`/users/${classId}/gradesbis/${this.user_id}`);
      const grades = response.data;
      console.log(`Grades for class ${classId}:`, grades); // Add this log to check grades

      // Use the spread operator to create a new object with the new property
      this.gradesByClassId = { ...this.gradesByClassId, [classId]: grades.grade };
    }
  } catch (error) {
    console.error("Error fetching grades for classes:", error);
  }
}

  },
};
</script>

<style></style>
