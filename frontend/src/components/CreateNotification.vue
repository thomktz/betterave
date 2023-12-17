<template>
    <div class="notification-creation-panel">
      <v-container class="create-notification-container">
        <v-form @submit.prevent="handleCreateNotification">
          <v-text-field
            label="Notification Title"
            v-model="notificationData.title"
            required
          ></v-text-field>
  
          <v-text-field
            label="Notification Content"
            v-model="notificationData.content"
            required
          ></v-text-field>
  
          <v-select
            :items="recipientOptions"
            label="Recipients"
            class="recipient-dropdown"
            v-model="selectedRecipient"
          ></v-select>
  
          <v-btn type="submit" class="create-notification-button">Create Notification</v-btn>
        </v-form>
      </v-container>
    </div>
  </template>
  
  <script>
  import { ref, computed, watch } from "vue";
  import { toast } from "@/apiConfig";
  
  export default {
    props: {
      user_id: {
        type: Number,
        required: true,
      },
      user_type: {
        type: String,
        required: true,
      },
    },
    setup(props, { emit }) {
      const notificationData = ref({
        sent_by_user_id: props.user_id,
        title: "",
        content: "",
        recipient_type: "",
      });
  
      const selectedRecipient = ref(null);
  
      watch(selectedRecipient, (newValue) => {
        notificationData.value.recipient_type = newValue;
      });
  
      const recipientOptions = computed(() => {
        if (props.user_type === "admin") {
          return ["All users", "Subscribers", "1A", "2A", "3A"];
        }
        selectedRecipient.value = "Subscribers";
        return ["Subscribers"];
      });
  
      const handleCreateNotification = () => {
        // Ensure that all fields are filled, display toast if not
        if (
          !notificationData.value.title ||
          !notificationData.value.content ||
          !selectedRecipient.value
        ) {
          toast.error("Please fill all fields");
          return "";
        }
        console.log("Submitting notification data:", notificationData.value);
        emit("submitNotification", notificationData.value);
  
        // Reset the form
        notificationData.value = {
          sent_by_user_id: props.user_id,
          title: "",
          content: "",
          recipient_type: "",
        };
        selectedRecipient.value = null;
      };
  
      return {
        notificationData,
        handleCreateNotification,
        recipientOptions,
        selectedRecipient,
      };
    },
  };
  </script>
  
  <style>
  .notification-creation-panel {
    float: right;
    width: 50%;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background: var(--foreground-color);
  }
  
  .create-notification-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }
  
  .create-notification-button {
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
    font-family: "Montserrat", sans-serif !important;
  }
  .create-notification-button:hover {
    background-color: darken(var(--v-input-background-color), 10%) !important;
    color: var(--primary-text-color) !important;
  }
  .recipient-dropdown {
    margin-top: 22px !important;
  }
  </style>
  