<template>
  <div class="event-creation-panel">
    <v-container class="create-event-container">
      <v-form @submit.prevent="handleCreateEvent">
        
        <v-text-field
          label="Event Name"
          v-model="eventData.name"
          required
        ></v-text-field>

        <v-text-field
          v-model="formattedDate"
          label="Event Date"
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
            v-model="eventData.date" 
            @update:model-value="showDatePicker = false"
            :first-day-of-week="1"
          ></v-date-picker>
        </v-dialog>
        <div class="timepickers">
          <vue-timepicker
            :key="startTimePickerKey"
            v-model="eventData.start_time"
            label="Start Time"
            required
            format="HH:mm"
            minute-interval="5"
            :hour-range="[[7, 22]]"
            class="time-picker"
            :hideDisabledHours="true"
            placeholder="  Start time"
          ></vue-timepicker>

          <vue-timepicker
            :key="endTimePickerKey"
            v-model="eventData.end_time"
            label="End Time"
            required
            format="HH:mm"
            minute-interval="5"
            :hour-range="[[7, 22]]"
            class="time-picker"
            :hideDisabledHours="true"
            placeholder="  End time"
          ></vue-timepicker>
        </div>

        <v-select
          :items="participantOptions"
          :disabled="isDropdownDisabled"
          label="Participants"
          class="participant-dropdown"
          v-model="selectedParticipant"
        ></v-select>

        <v-btn type="submit" class="create-event-button">Create Event</v-btn>
      </v-form>
    </v-container>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { toast } from '@/apiConfig';
import VueTimepicker from 'vue3-timepicker';
import 'vue3-timepicker/dist/VueTimepicker.css';

export default {
  components: {
    VueTimepicker
  },
  props: {
    user_id: {
      type: Number,
      required: true
    },
    user_type: {
      type: String,
      required: true
    }
  },
  setup(props, { emit }) {
    const startTimePickerKey = ref(0);
    const endTimePickerKey = ref(0);
    const eventData = ref({
      asso_id: props.user_id,
      name: '',
      date: null,
      start_time: '',
      end_time: '',
      description: '',
      location: '',
      participants: ''
    });

    const selectedParticipant = ref(null);

    watch(selectedParticipant, (newValue) => {
      eventData.value.participants = newValue;
    });

    const participantOptions = computed(() => {
      if (props.user_type === "admin") {
        return ["All users", "1A", "2A", "3A"];
      }
      selectedParticipant.value = "Subscribers";
      return ["Subscribers"];
    });

    const isDropdownDisabled = computed(() => {
      return props.user_type !== "admin";
    });


    const formatDate = (dateStr) => {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
      return date.toLocaleDateString('en-US', options);
    };

    const formattedDate = computed(() => {
      return formatDate(eventData.value.date);
    });

    const showDatePicker = ref(false);

    const handleCreateEvent = () => {
      // Ensure that all fields are filled, display toast if not
      if (!eventData.value.name || !eventData.value.date || !eventData.value.start_time || !eventData.value.end_time || !selectedParticipant.value) {
        toast.error('Please fill all fields');
        return '';
      }
      console.log("Submitting event data:", eventData.value)
      emit('submitEvent', eventData.value);

      // Reset the form
      eventData.value = {
        asso_id: props.user_id,
        name: '',
        date: null,
        start_time: '',
        end_time: '',
        description: '',
        location: '',
        participants: ''
      };
      selectedParticipant.value = null;
      // Force re-render of the timepickers
      startTimePickerKey.value++;
      endTimePickerKey.value++;
    };

    return { eventData, 
      showDatePicker, 
      handleCreateEvent, 
      formatDate, 
      formattedDate, 
      startTimePickerKey, 
      endTimePickerKey,
      participantOptions,
      isDropdownDisabled,
      selectedParticipant
     };
  }
}
</script>

<style>
.event-creation-panel {
  float: right;
  width: 50%;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background: var(--foreground-color);
}

.create-event-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

.timepickers {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}
.time-picker {
  flex: 1 1 50%;
  max-width: calc(50% - 10px);
}
.vue__time-picker input.vue__time-picker-input {
  border: none;
  border-bottom: 1px solid var(--v-input-border-color);
  background-color: var(--v-input-background-color);
  height: 50px;
  min-width: 100%;
}
.time-picker input {
  color: var(--v-input-text-color);
  font-family: 'Montserrat', sans-serif;
}
.time-picker .vue__time-picker-input.is-empty::placeholder {
  color: var(--v-input-text-color);
}
.create-event-button {
  margin-top: 15px !important;
  height: 45px !important;
  margin-left: auto !important;
  margin-right: auto !important;
  background-color: var(--v-input-background-color) !important;
  color: var(--v-input-text-color) !important;
  border: 1px solid var(--v-input-border-color) !important;
  padding: 10px 20px !important;
  border-radius: 20px !important;
  cursor: pointer;
  font-size: 1em !important;
  transition: background-color 0.3s !important;
  width: 90% !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  text-align: center !important;
  box-shadow: none !important;
  font-family: 'Montserrat', sans-serif !important;
}
.create-event-button:hover {
  background-color: darken(var(--v-input-background-color), 10%) !important;
  color: var(--primary-text-color) !important;
}
.participant-dropdown {
  margin-top: 22px !important;
}
</style>

