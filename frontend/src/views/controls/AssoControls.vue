<template>
  <v-container class="fill-height" fluid>
    <div class="main-container">
      <div class="events-list">
        <v-list v-if="events.length > 0" dense>
          <v-list-item
            v-for="event in events"
            :key="event.id"
            class="event-pill"
            appendIcon="mdi-delete"
            @click="deleteEvent(event)"
          >
            <div class="event-content">
              <h3 class="event-title">{{ event.title }}</h3>
              <p class="event-subtitle">
                {{ formatEventTimes(event.start, event.end) }}
              </p>
            </div>
          </v-list-item>
        </v-list>
        <div v-else class="no-events">No events yet.</div>
      </div>
      <CreateEvent
        v-if="user_id"
        :user_id="user_id"
        :user_type="user_type"
        class="create-event-panel"
        @submitEvent="submitEvent"
      >
      </CreateEvent>
    </div>
  </v-container>
</template>

<script>
import CreateEvent from "@/components/CreateEvent.vue";
import { apiClient } from "@/apiConfig";
export default {
  components: {
    CreateEvent,
  },
  data() {
    return {
      user_id: null,
      user_type: null,
      events: [], // Placeholder for events data
    };
  },
  async mounted() {
    this.$emit("updateTitle", `Association Controls`);

    // Fetch the type of the current user (not the selected one!)
    const response = await apiClient.get(`/users/me`);
    this.user_id = response.data.user_id;
    this.user_type = response.data.user_type;

    // Fetch events
    const eventsResponse = await apiClient.get("/users/me/events/future");
    this.events = eventsResponse.data; // Assume the response has the data in this format
  },
  methods: {
    formatEventTimes(start, end) {
      const startDate = new Date(start);
      const endDate = new Date(end);
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return `${startDate.toLocaleDateString(
        "en-US",
        options,
      )} - ${endDate.toLocaleDateString("en-US", options)}`;
    },
    async submitEvent(eventData) {
      const date = eventData.date;
      const year = date.getFullYear();
      const month = date.getMonth() + 1; // getMonth() returns 0-11, so add 1 for the correct month
      const day = date.getDate();

      // Format the date as YYYY-MM-DD
      const formattedDate = `${year}-${month.toString().padStart(2, "0")}-${day
        .toString()
        .padStart(2, "0")}`;

      const data = {
        asso_id: this.user_id,
        name: eventData.name,
        date: formattedDate,
        start_time: eventData.start_time,
        end_time: eventData.end_time,
        description: eventData.description,
        location: eventData.location,
        participants: eventData.participants,
      };
      console.log(data);

      try {
        const response = await apiClient.post("/events/", data);
        this.events.push(response.data);
      } catch (error) {
        console.error("Error adding event:", error);
      }
    },
    async deleteEvent(event) {
      try {
        await apiClient.delete(`/events/${event.event_id}`);
        this.events = this.events.filter((e) => e.event_id !== event.event_id);
      } catch (error) {
        console.error("Error deleting event:", error);
        // Handle error
      }
    },
  },
};
</script>

<style>
.main-container {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px;
  width: 100%;
}

.events-list {
  flex: 0 0 45%;
  background-color: var(--foreground-color);
  min-height: 100px;
  padding: 20px;
  box-sizing: border-box;
  border-radius: 15px;
  overflow-y: auto;
}
.v-list {
  background-color: var(--foreground-color) !important;
}

.event-pill {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  margin-bottom: 10px !important;
  padding: 10px !important;
  border: 1px solid var(--text-bubble-color) !important;
  border-radius: 15px !important;
  background-color: var(--v-input-background-color) !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.event-content {
  flex-grow: 0;
  padding-right: 10px; /* Add some padding if needed */
}

.event-title {
  font-weight: bold;
  margin: 0;
}

.event-subtitle {
  font-size: 0.85rem;
  margin: 0;
}

.no-events {
  text-align: center;
  color: var(--secondary-text-color);
  font-style: italic;
}
.create-event-panel {
  flex: 0 0 45%;

  padding: 20px;
  border-radius: 15px;
}
.event-pill:hover .v-icon {
  color: red;
}
</style>
