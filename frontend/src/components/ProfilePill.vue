<template>
<div class="profile-pill" @mouseover="showDropdown = true" @mouseleave="showDropdown = false">
    <div class="email-with-icon">
    <img src="/default-profile.png" alt="Profile Icon" class="profile-icon" />
    <span>{{ userEmail }}</span>
    </div>
    <div v-if="showDropdown" class="dropdown-content">
    <button @click="logout">Logout</button>
    </div>
</div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      userEmail: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        showDropdown: false
      };
    },
    methods: {
      async logout() {
        try {
          await axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true });
          this.$router.push({ name: 'Login' });
        } catch (error) {
          console.error("There was an error logging out:", error);
        }
      }
    }
  }
  </script>

<style scoped>
.profile-pill {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  border-radius: 25px;
  cursor: pointer;
  position: relative;
}

.profile-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.dropdown-content {
  display: block;
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ffffff;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content button {
  background: none;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  display: block;
  width: 100%;
  text-align: left;
}

.email-with-icon {
    display: flex;
    align-items: center;
}
</style>