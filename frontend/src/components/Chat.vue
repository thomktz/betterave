<template>
    <div>
      <div v-for="message in messages" :key="message.id">
        <b>{{ message.student_name }}</b>: {{ message.content }}
      </div>
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message...">
      <button @click="sendMessage">Send</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';


  export default {
    props: {
      classId: {
        type: String,
        required: true,
      }
    },
    data() {
      return {
        messages: [],
        newMessage: '',
      };
    },
    mounted() {
      this.fetchClassMessages();
    },
    methods: {
      async fetchClassMessages() {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/classes/${this.classId}/messages`, { withCredentials: true });
          
          if (response.data && Array.isArray(response.data)) {
            this.messages = response.data;
          }
        } catch (error) {
          console.error("There was an error fetching class messages:", error);
          // Handle error (e.g., showing an error message to the user)
        }
      },
      async sendMessage() {
        if (!this.newMessage.trim()) return;  // Don't send empty messages

        try {
          const response = await axios.post(`http://127.0.0.1:5000/classes/${this.classId}/messages`, 
            { content: this.newMessage }, 
            { withCredentials: true }
          );

          if (response.data && response.data.status === "success") {
            this.messages.push({
              id: response.data.messageId,  // assuming the backend returns the new message's id
              content: this.newMessage
            });
            this.newMessage = '';  // Clear the input after successful send
          }
        } catch (error) {
          console.error("There was an error sending the message:", error);
          // Handle error (e.g., showing an error message to the user)
        }
      },
    },
  };
  </script>
  