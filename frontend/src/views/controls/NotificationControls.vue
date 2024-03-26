<template>
    <v-container class="fill-height" fluid>
      <div class="main-container">
        <div class="notifications-list">
          <v-list v-if="notifications.length > 0" dense>
            <v-list-item
              v-for="notification in notifications"
              :key="notification.notification_id"
              class="notification-pill"
              appendIcon="mdi-delete"
              @click="deleteNotification(notification)"
            >
              <div class="notification-content">
                <h3 class="notification-title">{{ notification.title }}</h3>
                <p class="notification-subtitle">{{ notification.content }}</p>
              </div>
            </v-list-item>
          </v-list>
          <div v-else class="no-notifications">No notifications yet.</div>
        </div>
        <CreateNotification
          v-if="user_id"
          :user_id="user_id"
          :user_type="user_type"
          class="create-notification-panel"
          @submitNotification="submitNotification"
        >
        </CreateNotification>
      </div>
    </v-container>
  </template>
  
  <script>
  import CreateNotification from "@/components/CreateNotification.vue";
  import { apiClient } from "@/apiConfig";
  
  export default {
    components: {
      CreateNotification,
    },
    data() {
      return {
        user_id: null,
        user_type: null,
        notifications: [], // Placeholder for notifications data
      };
    },
    async mounted() {
      this.$emit("updateTitle", "Notification Controls");
  
      // Fetch the type of the current user (not the selected one!)
      const response = await apiClient.get("/users/me");
      this.user_id = response.data.user_id;
      this.user_type = response.data.user_type;
  
      // Fetch notifications
      const notificationsResponse = await apiClient.get("/users/me/notifications");
      this.notifications = notificationsResponse.data; // Assume the response has the data in this format
    },
    methods: {
      async submitNotification(notificationData) {
        const data = {
          title: notificationData.title,
          content: notificationData.content,
          sent_by_user_id: this.user_id,
          recipient_type: notificationData.recipient_type,
        };
      console.log(data);
  
        try {
          const response = await apiClient.post("/notifications/", data);
          this.notifications.push(response.data);
        } catch (error) {
          console.error("Error adding notification:", error);
        }
      },
      async deleteNotification(notification) {
        try {
          await apiClient.delete(`/notifications/${notification.notification_id}`);
          this.notifications = this.notifications.filter(
            (n) => n.notification_id !== notification.notification_id
          );
        } catch (error) {
          console.error("Error deleting notification:", error);
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
  
  .notifications-list {
    flex: 0 0 45%;
    background-color: var(--foreground-color);
    min-height: 100px;
    padding: 20px;
    box-sizing: border-box;
    border-radius: 15px;
    overflow-y: auto;
  }
  
  .notification-pill {
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

  .notification-content {
    flex-grow: 0;
    padding-right: 10px; /* Add some padding if needed */
  }

  .notification-title {
    font-weight: bold;
    margin: 0;
  }

  .notification-subtitle {
    font-size: 0.85rem;
    margin: 0;
  }

  .no-notifications {
    text-align: center;
    color: var(--secondary-text-color);
    font-style: italic;
  }

  .create-notification-panel {
    flex: 0 0 45%;
    padding: 20px;
    border-radius: 15px;
  }

  .notification-pill:hover .v-icon {
    color: red;
  }
</style>
