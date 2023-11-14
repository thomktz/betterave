<template>
  <v-container class="fill-height" fluid>
    <div class="content-container">
      <!-- Left Side Columns -->
      <div class="columns-container">
        <ColumnNextclasses :user="user" title="Next classes" />
        <InfoColumn title="Homework" :list="homeworkList" />
        <InfoColumn title="Notifications" :list="notifications" />
      </div>

      <!-- Right Side Calendar -->
      <div class="calendar-box">
        <UserCalendar :user="user" />
      </div>
    </div>
  </v-container>
</template>

<script>
import { apiClient } from '@/apiConfig';
import UserCalendar from '@/components/UserCalendar.vue';
import InfoColumn from '@/components/InfoColumn.vue';
import ColumnNextclasses from '@/components/ColumnNextclasses.vue';

export default {
  components: {
    UserCalendar,
    InfoColumn,
    ColumnNextclasses,
  },
  data() {
    return {
      user: {
        name: '',
        email: ''
      },
      homeworkList: [{ id: 1, text: "Algebra homework" }, { id: 2, text: "Essay on WW2" }],
      notifications: [{ id: 1, text: "Meeting tomorrow" }, { id: 2, text: "Homework due" }]
    };
  },
  async mounted() {
    const response = await apiClient.get('/users/me');
    this.user = response.data;
    this.$emit('updateTitle', "Hello, " + this.user.name + "!");
  },
  methods: {

  }
}
</script>

<style scoped>
.calendar-box {
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  width: calc(50% - 20px);
  overflow: hidden;
  height: 70vh;
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
  height: 70vh;
}
</style>