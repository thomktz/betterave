<template>
  <v-container class="fill-height" fluid>
    <div class="content-container">
      <!-- Left Side Columns -->
      <div class="columns-container">
        <ColumnNextclasses :user="user" title="Next classes" />
        <!-- Middle Container -->
        <div class="main-column">
          <h2>Homework</h2>
          <Homework></Homework>
        </div>
      </div>


        <div class="notification-container">
          <h2>Notifications</h2>
         <!-- Ajoutez le contenu de votre composant de notification ici si nécessaire -->
         </div>

    


      <!-- Right Side Calendar -->
      <div class="calendar-box">
        <UserCalendar :user="user" />
      </div>
    </div>
  </v-container>
</template>

<script>
import { apiClient } from "@/apiConfig";
import UserCalendar from "@/components/UserCalendar.vue";
import InfoColumn from "@/components/InfoColumn.vue";
import ColumnNextclasses from "@/components/ColumnNextclasses.vue";
import Homework from "@/components/Homework.vue";

export default {
  components: {
    UserCalendar,
    InfoColumn,
    ColumnNextclasses,
    Homework,
  },
  data() {
    return {
      user: {
        name: "",
        email: "",
      },
      homeworkList: [
        { id: 1, text: "Algebra homework" },
        { id: 2, text: "Essay on WW2" },
      ],
      notifications: [
        { id: 1, text: "Meeting tomorrow" },
        { id: 2, text: "Homework due" },
      ],
    };
  },
  async mounted() {
    const response = await apiClient.get("/users/me");
    this.user = response.data;
    this.$emit("updateTitle", "Hello, " + this.user.name + "!");
  },
  methods: {},
};
</script>

<style>

.notification-container {
  justify-content: space-between;
  width: calc(50% - 20px);
  height: 80vh;
  padding: 20px;
  background-color: var(--secondary-color-transparent);
  color: var(--primary-text-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  margin: 0 10px;
  
}

.notification-container h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--separator-color);
  padding-bottom: 10px;
}



.calendar-box {
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  width: calc(50% - 20px);
  overflow: hidden;
  height: 80vh;
}

.content-container {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  width: 100%;
}

.columns-container {
  display: flex;
  justify-content: space-between;
  width: calc(50% - 20px);
  height: 80vh;
}
.main-column {
  flex: 1.5;
  padding: 20px;
  background-color: var(--secondary-color-transparent);
  color: var(--primary-text-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  margin: 0 10px;
  overflow-y: auto;
  position: relative;
  z-index: 1;
}
h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--separator-color);
  padding-bottom: 10px;
}
</style>
