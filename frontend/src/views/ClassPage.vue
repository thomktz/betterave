<template>
  <div class="fill-height" fluid>
    <div class="content-section">
      <!-- Left Container -->
      <div class="info-container">
        <div class="class-header">
          <h1>Class details</h1>
        </div>
        <p><strong>ECTS Credits:</strong> {{ classDetails.ects_credits }}</p>
        <p><strong>Tutor:</strong> {{ classDetails.teacher }}</p>
        <p>
          <a :href="classDetails.ensae_link" target="_blank">View ENSAE Link</a>
        </p>

        <!-- Edit grades only available for teachers and admins -->
        <div
          v-if="user_type == 'teacher' || user_type == 'admin'"
          class="edit-container"
          @click="redirectToEditGrades"
        >
          <span><h1>Edit Grades</h1></span>
          <v-icon class="edit-icon">mdi-pencil</v-icon>
        </div>

        <!-- Edit homexorks only available for teachers and admins -->
        <div
          v-if="user_type == 'teacher' || user_type == 'admin'"
          class="edit-container"
          @click="openAddHomeworkDialog"
        >
          <span><h1>Add Homework</h1></span>
          <v-icon class="edit-icon">mdi-pencil</v-icon>

          <!-- Dialog for adding new homework -->
          <v-dialog v-model="dialogVisible" max-width="500px">
            <v-card>
              <v-card-title>Add Homework</v-card-title>
              <v-card-text>
                <v-text-field
                  v-model="formattedDate"
                  label="Due Date"
                  readonly
                  @click="showDatePicker = true"
                  @focus="showDatePicker = true"
                  required
                ></v-text-field>

                <v-dialog
                  v-model="showDatePicker"
                  persistent
                  width="290px"
                  @click:outside="showDatePicker = false"
                >
                  <v-date-picker
                    v-model="newHomework.due_date"
                    @update:model-value="showDatePicker = false"
                    :first-day-of-week="1"
                  ></v-date-picker>
                </v-dialog>

                <vue-timepicker
                  :key="dueTimePickerKey"
                  v-model="newHomework.due_time"
                  label="Due Time"
                  required
                  format="HH:mm"
                  minute-interval="1"
                  class="time-picker"
                  :hideDisabledHours="true"
                  placeholder="  Due time"
                ></vue-timepicker>

                <v-text-field
                  v-model="newHomework.content"
                  label="Homework Content"
                ></v-text-field>
              </v-card-text>
              <v-card-actions>
                <v-btn @click="saveHomework" color="primary">Save</v-btn>
                <v-btn @click="closeDialog">Cancel</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </div>
      </div>

      <!-- Middle Container -->
      <div class="info-container">
        <div class="class-header">
          <h1>Homework</h1>
        </div>
        <Homework :class_id="class_id"></Homework>
      </div>

      <!-- Right Container -->
      <div class="info-container">
        <Chat :class_id="class_id" :user_id="user_id"></Chat>
      </div>
    </div>
  </div>
</template>

<script>
import Chat from "@/components/Chat.vue";
import { apiClient } from "@/apiConfig";
import Homework from "@/components/Homework.vue";

export default {
  components: {
    Homework,
    Chat,
  },
  data() {
    return {
      classDetails: {},
      class_id: parseInt(this.$route.params.class_id),
      user_id: NaN,
      user_type: "student",
      dialogVisible: false,
      newHomework: {
        content: "",
        due_date: null,
      },
    };
  },
  async mounted() {
    try {
      const response = await apiClient.get(`/classes/${this.class_id}`);
      this.classDetails = response.data;
      this.$emit("updateTitle", `${this.classDetails.name}`);
    } catch (error) {
      console.error("Error fetching class details:", error);
    }
    try {
      const response = await apiClient.get("/users/me");
      this.user_id = response.data.user_id;
      this.user_type = response.data.user_type;
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  },
  methods: {
    async saveHomework() {
      try {
        if (this.class_id) {
          const date = this.newHomework.due_date;
          const year = date.getFullYear();
          const month = date.getMonth() + 1; // getMonth() returns 0-11, so add 1 for the correct month
          const day = date.getDate();

          // Format the date as YYYY-MM-DD
          const formattedDate = `${year}-${month
            .toString()
            .padStart(2, "0")}-${day.toString().padStart(2, "0")}`;

          console.log("Formatted date:", formattedDate);

          const response = await apiClient.post(
            `/classes/${this.class_id}/homework`,
            {
              content: this.newHomework.content,
              class_id: this.class_id,
              due_date: formattedDate,
              due_time: this.newHomework.due_time,
            },
          );
          console.log("API Response:", response.data);
          this.closeDialog();
        }
      } catch (error) {
        console.error("Error adding homework:", error);
      }
    },
    redirectToEditGrades() {
      // Navigate to the 'edit-grades' route
      this.$router.push(`/class/${this.class_id}/grades`);
    },
    openAddHomeworkDialog() {
      // Open the dialog when the "Add Homework" button is clicked
      this.dialogVisible = true;
    },
    closeDialog() {
      // Close the dialog and reset form values
      this.dialogVisible = false;
      this.newHomework = {
        content: "",
        due_date: null,
      };
    },
  },
};
</script>

<style scoped>
.content-section {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 20px;
}

.info-container {
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  width: calc(33.333% - 30px); /* Adjusting for the space between containers */
  padding: 20px;
  height: 80vh;
}

.class-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 20px; /* space between title and content */
}
.edit-container {
  cursor: pointer;
  display: flex;
  align-items: center;
  color: var(--primary-text-color);
}

.edit-container span {
  margin-right: 10px;
}

.edit-icon {
  font-size: 2rem;
}
</style>
