<template>
<div class="profile-pill" @mouseover="showDropdown = true" @mouseleave="showDropdown = false">
    <div class="email-with-icon">
    <img v-if="user && user.profile_pic" :src="'/' + user.profile_pic" alt="Profile Icon" class="profile-icon" />
    <span>{{ user.email }}</span>
    </div>
    <div v-if="showDropdown" class="dropdown-content">
      <router-link to="/" class="dropdown-link">Home</router-link>
      <router-link to="/photochart" class="dropdown-link">Trombinoscope</router-link>
      <router-link to="/assolist" class="dropdown-link">Associations</router-link>
      <button v-if="user.user_type == 'admin'" @click="goToAdminControls">Manage students</button>
      <button v-if="user.user_type == 'asso' || user.user_type == 'admin'" @click="goToAssoControls">Manage events</button>
      <button v-if="user.user_type == 'student'" @click="goToStudentControls">Manage courses</button>
      <button @click="logout">Logout</button>
    </div>
</div>
</template>
  
  <script>
import { apiClient, toast } from '@/apiConfig';
  
  export default {
    props: {
      user: {
        type: Object,
        required: true
      },
    },
    data() {
      return {
        showDropdown: false
      };
    },
    methods: {
      async logout() {
        apiClient.post('/auth/logout')
        .then(response => {
          this.$router.push({ name: 'Login' });
        });
      },
      goToAdminControls() {
        this.$router.push({ name: 'admin-controls' });
      },
      goToAssoControls() {
        this.$router.push({ name: 'asso-controls' });
      },
      goToStudentControls() {
        this.$router.push({ name: 'student-controls' });
      }
    }
  }
  </script>

<style scoped>
.profile-pill {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #2f5b5b; 
  color: #ffffff; 
  border-radius: 25px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.3s; 
}

.profile-pill:hover {
  background-color: #4596a6; 
}

.profile-icon {
  width: 45px;
  height: 45px;
  border-radius: 100%;
  margin-right: 20px;
}

.dropdown-content {
  display: block;
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333; 
  color: #ffffff; 
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  border-radius: 8px; 
  width: 80%;
  z-index: 9999; 

}

.dropdown-content button {
  background: none;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  display: block;
  width: 100%;
  text-align: left;
  transition: background-color 0.3s; 
}

.dropdown-content button:hover {
  background-color: #555; 
}

.dropdown-link {
  display: block;
  padding: 10px 20px;
  color: #ffffff; 
  transition: background-color 0.3s; 
  text-decoration: none; 
}

.dropdown-link:hover {
  background-color: #555; 
}

.email-with-icon {
  display: flex;
  align-items: center;
}

</style>