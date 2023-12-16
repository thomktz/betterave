<template>
  <v-container class="main-container">
    <v-container class="inner-container">
      <v-row align="stretch" class="row">
      </v-row>

      <!-- Classes Table -->
      <v-data-table
        :headers="headers"
        :items="classes"
        class="elevation-1"
        density="compact"
      >


      </v-data-table>
    </v-container>
  </v-container>


</template>

<script>
export default {
  props: {
    classes: Array,
    availableClasses: Array,
    asAdmin: Boolean,
  },
  emits: [
    "request-classes",
    "enroll-class",
    "update-class-group",
    "delete-class",
  ],
  data() {
    return {
      headers: [
        { title: "Class Name", value: "class_name" },
        { title: "ECTS", value: "class_ects" },
        { title: "Grades", value: "secondary_class_group_name" },
        { title: "", value: "actions", sortable: false },
      ],
      dialog: false,
      selectedId: null,
    };
  },
  computed: {
    totalECTS() {
      return this.classes.reduce(
        (total, classItem) => total + classItem.class_ects,
        0,
      );
    },
    ectsColor() {
      const total = this.totalECTS;
      return total >= 30 && total <= 32 ? "green" : "red";
    },
  },
  methods: {
    onButtonClick() {
      this.$emit("request-classes");
      this.dialog = true;
    },
    enroll() {
      this.$emit("enroll-class", this.selectedId);
      this.selectedId = null;
      this.dialog = false;
    },
    emitDeleteClass(class_id) {
      this.$emit("delete-class", class_id);
    },
    emitUpdateClass(item) {
      this.$emit("update-class-group", {
        class_id: item.class_id,
        secondaryClassGroupName: item.secondary_class_group_name,
      });
    },
    getGroupName(item) {
      return item.secondary_class_group_name ? "Secondary group" : "No groups";
    },
  },
};
</script>

<style scoped>
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

.custom-circle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background-color: #1d958b;
  border-radius: 50%;
  transition:
    background-color 0.3s,
    transform 0.3s;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
  margin-left: auto;
  margin-right: 20px;
}

.custom-circle-btn:hover {
  background-color: #3bc8bc;
  transform: scale(1.1);
}

.custom-circle-btn v-icon {
  color: white;
}

.custom-circle-btn:hover v-icon {
  transform: rotate(90deg);
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
.icon-btn {
  background-color: var(--secondary-color);
}
</style>
