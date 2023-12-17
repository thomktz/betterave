<template>
    <div class="notifications-column">
      <h2>{{ title }}</h2>
      <ul>
        <li v-for="(notification, index) in notifications" :key="notification.notification_id">
          <div
            class="date-indicator"
            v-if="isFirstNotificationOfDay(notifications, index)"
          >
            {{ formatDate(notification.created_at) }}
          </div>
          <div
            :style="getNotificationStyle(notification)"
            class="notification-item"
          >
            <div class="notification-content">
              <div class="notification-title">{{ notification.title }}</div>
              <div class="notification-sender">
                Sent by {{ notification.sender.username }}
              </div>
            </div>
            <div class="notification-buttons">
              <v-icon @click="deleteNotification(notification)">
                mdi-delete
              </v-icon>
              <v-icon @click="editNotification(notification)">
                mdi-pencil
              </v-icon>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import { apiClient } from "@/apiConfig";
  import { toast } from "@/utils";
  
  const limit = 50;
  
  export default {
    props: {
      user: {
        type: Object,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        notifications: [],
        // Add other necessary data properties here
      };
    },
    async mounted() {
      // Fetch notifications
      try {
        const response = await apiClient.get("/notifications/");
        this.notifications = response.data;
      } catch (error) {
        console.error("Error fetching notifications:", error);
        // Handle error
      }
    },
    methods: {
      // Add other necessary methods here
  
      // Example methods for illustration purposes
      deleteNotification(notification) {
        // Implement delete logic
        // Show toast for success or error
        toast.success("Notification deleted successfully");
      },
      editNotification(notification) {
        // Implement edit logic
        // Show toast for success or error
        toast.success("Notification edited successfully");
      },
  
      getNotificationStyle(notification) {
        return {
          backgroundColor: notification.backgroundColor || "#4868bf", // Default color
        };
      },
      isFirstNotificationOfDay(list, index) {
        if (index === 0) {
          return true;
        } else {
          const currentStartTime = new Date(list[index].created_at).setHours(
            0,
            0,
            0,
            0,
          );
          const previousStartTime = new Date(
            list[index - 1].created_at,
          ).setHours(0, 0, 0, 0);
          return currentStartTime !== previousStartTime;
        }
      },
      formatDate(date) {
        // Date format 'dd/mm/yyyy'
        const eventDate = new Date(date);
        const options = { weekday: "long", month: "long", day: "numeric" };
        return eventDate.toLocaleDateString("en-US", options);
      },
    },
  };
  </script>
  
  <style scoped>
  .notifications-column {
    flex: 1.5;
    padding: 20px;
    background-color: var(--secondary-color);
    color: var(--primary-text-color);
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    margin: 0 10px;
    overflow-y: auto;
  }
  
  h2 {
    font-size: 1.5rem;
    margin-bottom: 20px;
    border-bottom: 1px solid #b0b0b0;
    padding-bottom: 10px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  
  .notification-item {
    display: flex;
    flex-direction: column;
    padding: 10px;
    border-radius: 10px;
    color: rgb(0, 0, 0);
    margin-top: 10px;
    cursor: pointer;
  }
  
  .notification-content {
    margin-top: 10px;
    font-size: 0.8rem;
  }
  
  .notification-title {
    font-size: 1rem;
    font-weight: bold;
    margin: 0;
  }
  
  .notification-sender {
    font-size: 0.8rem;
    margin: 5px 0;
  }
  
  .notification-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
  }
  
  .notification-buttons v-icon {
    cursor: pointer;
  }
  
  .date-indicator {
    display: flex;
    align-items: center;
    padding: 0;
    font-size: 0.8rem;
    position: relative;
    margin-top: 12px;
    margin-bottom: -5px;
    background-color: transparent;
  }
  
  .date-indicator::after {
    content: "";
    flex-grow: 1;
    height: 1px;
    background-color: #b0b0b0;
    margin-left: 10px;
  }
  </style>
  
  