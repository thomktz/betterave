<template>
  <section class="msger">
    <main class="msger-chat" ref="chatContainer">
      <div 
        v-for="message in messages" 
        :key="message.id" 
        :class="message.user_id === userId ? 'msg right-msg' : 'msg left-msg'"
        @mouseover="showDate(message)" 
        @mouseleave="hideDate()"
      >
        <img :src="'/' + message.user_profile_pic" :alt="message.user_name" class="msg-img" />
        <div class="whole-message">
          <div class="msg-name">{{ message.user_name }} {{ message.user_surname }}</div>
          <div class="msg-text">{{ message.content }}</div>
          <div class="msg-date" v-show="hoveredMessageId === message.id">{{ formatDate(message.timestamp) }}</div>
        </div>
      </div>
    </main>
    <form class="msger-inputarea" @submit.prevent="sendMessage">
      <input type="text" v-model="newMessage" class="msger-input" placeholder="Enter your message..." @keyup.enter="sendMessage">
      <button type="submit" class="msger-send-btn">Send</button>
    </form>
  </section>
</template>
  
  <script>
  import axios from 'axios';
  import { format } from 'date-fns';


  export default {
    props: {
      classId: {
        type: String,
        required: true,
      },
      userId: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        messages: [],
        newMessage: '',
        hoveredMessageId: null,
        
      };
    },
    mounted() {
      this.fetchClassMessages();
      this.scrollToBottom();
    },
    methods: {
      formatDate(isoString) {
        return format(new Date(isoString), 'yyyy-MM-dd HH:mm');
      },
      showDate(message) {
        this.hoveredMessageId = message.id;
      },
      hideDate() {
        this.hoveredMessageId = null;
      },
      scrollToBottom() {
        this.$nextTick(() => {
          this.$refs.chatContainer.scrollTop = this.$refs.chatContainer.scrollHeight;
        });
      },
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
        this.scrollToBottom();
      },
      async sendMessage() {
        if (!this.newMessage.trim()) return;  // Don't send empty messages
        try {
          const response = await axios.post(`http://127.0.0.1:5000/classes/${this.classId}/messages`, 
            { content: this.newMessage }, 
            { withCredentials: true }
          );
          this.newMessage = ''
        } catch (error) {
          console.error("There was an error sending the message:", error);
          // Handle error (e.g., showing an error message to the user)
        }
        this.fetchClassMessages()
      },
    },
  };
  </script>
  
  <style scoped>
/* General styling */
.msger {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 5px;
  overflow: hidden;
  font-family: 'Arial', sans-serif;
}

/* Chat styling */
.msger-chat {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #f5f5f5;
}

.msger-chat::-webkit-scrollbar {
  width: 6px;
}

.msger-chat::-webkit-scrollbar-track {
  background: #ddd;
}

.msger-chat::-webkit-scrollbar-thumb {
  background: #bdbdbd;
}

.msg {
  display: flex;
  align-items: flex-end;
  margin-bottom: 18px;
}

.msg:last-of-type {
  margin: 0;
}

.msg-img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  background: #ddd;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
  border-radius: 50%;
  flex-shrink: 0;
}

.whole-message {
  max-width: 450px;
  position: relative;
}

.msg-name {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 5px;
  font-size: 0.8em;
  color: #4e4e4e;
}

.msg-text {
  border-radius: 20px;
  padding: 10px;
  font-size: 0.9em;
  word-wrap: break-word;
}

.left-msg .msg-text {
  background: #cdcdcd;
  border-bottom-left-radius: 0;
}
.left-msg .msg-name {
  justify-content: flex-start;
}

.right-msg {
  flex-direction: row-reverse;
}

.right-msg .msg-text {
  background: #0084ff;
  color: #fff;
  border-bottom-right-radius: 0;
}

.right-msg .msg-img {
  margin: 0 0 0 10px;
}

/* Input styling */
.msger-inputarea {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ddd;
  background: #eee;
}

.msger-inputarea * {
  padding: 10px;
  border: none;
  border-radius: 3px;
  font-size: 1em;
}

.msger-input {
  flex: 1;
  background: #ddd;
}

.msger-send-btn {
  margin-left: 10px;
  background: rgb(0, 196, 65);
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.23s;
}

.msger-send-btn:hover {
  background: rgb(0, 180, 50);
}

.msg-date {
  position: absolute;
  bottom: -18px; /* Adjust as needed to position the date appropriately below the message */
  left: 0;
  right: 0;
  white-space: nowrap;
  margin-top: 0; /* No margin needed since we're positioning it absolutely */
  font-size: 0.7em;
  color: rgb(113, 113, 113);
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.3s, visibility 0.3s;
}

.msg:hover .msg-date {
  opacity: 1;
  visibility: visible;
}


</style>