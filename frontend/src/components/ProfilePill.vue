<template>
<div class="profile-pill" @mouseover="showDropdown = true" @mouseleave="showDropdown = false">
    <div class="email-with-icon">
    <img :src="'/' + userProfilePic" alt="Profile Icon" class="profile-icon" />
    <span>{{ userEmail }}</span>
    </div>
    <div v-if="showDropdown" class="dropdown-content">
      <router-link to="/" class="dropdown-link">Home</router-link>
      <router-link to="/photochart" class="dropdown-link">Trombinoscope</router-link>
      <router-link to="/assolist" class="dropdown-link">Associations</router-link>
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
      },
      userProfilePic: {
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
          await axios.post('/logout', {}, { withCredentials: true });
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
  background-color: #2f5b5b; /* dark background */
  color: #ffffff; /* light text color */
  border-radius: 25px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.3s; /* smooth hover transition */
}

.profile-pill:hover {
  background-color: #4596a6; /* slightly lighter on hover */
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
  background-color: #333; /* dark background for consistency */
  color: #ffffff; /* light text color */
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
  border-radius: 8px; /* added border-radius for a modern touch */
  width: 80%;
  z-index: 9999; /* ensure the dropdown is on top of other elements */

}

.dropdown-content button {
  background: none;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  display: block;
  width: 100%;
  text-align: left;
  transition: background-color 0.3s; /* smooth hover transition for the button */
}

.dropdown-content button:hover {
  background-color: #555; /* slightly lighter on hover for the button */
}

.dropdown-link {
  display: block;
  padding: 10px 20px;
  color: #ffffff; /* light text color */
  transition: background-color 0.3s; /* smooth hover transition */
  text-decoration: none; /* remove underline */
}

.dropdown-link:hover {
  background-color: #555; /* slightly lighter on hover */
}

.email-with-icon {
  display: flex;
  align-items: center;
}

</style>