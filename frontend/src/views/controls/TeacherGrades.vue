<template>
    <v-container class="fill-height">
      <UserClassesTable
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
  import UserClassesTable from "@/components/UserGrades.vue";
  import { apiClient, toast } from "@/apiConfig";
  
  export default {
    components: {
      UserClassesTable,
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
      };
    },
    async mounted() {
      // Fetch the classes for the selected user
      const response = await apiClient.get(`/users/${this.user_id}/classgroups`);
      this.classesInfo = response.data;
      this.classes = this.classesInfo.classgroups;
      this.name = this.classesInfo.name;
      this.surname = this.classesInfo.surname;
      this.level = this.classesInfo.level;
  
      this.$emit("updateTitle", `${this.name} ${this.surname} Grades`);
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
    },
  };
  </script>
  
  <style></style>
  