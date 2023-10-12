<template>
  <div>
    <header class="header">
      <!-- Grouped Logos -->
      <div class="logos-block">
        <!-- Betterave Logo with Link to Home page -->
        <router-link to="/">
          <img src="/betterave-logo.png" alt="Betterave Logo" class="betterave-logo" title="Home page" />
        </router-link>
        
        <!-- ENSAE Logo with Link to ENSAE website -->
        <a href="https://www.ensae.fr/" target="_blank" rel="noopener noreferrer">
          <img src="/logo_ensae.png" alt="ENSAE Logo" class="ensae-logo" title="ENSAE website" />
        </a>
      </div>
      
      <h1>{{ headerTitle }}</h1>
      <ProfilePill :userEmail="user.email" :userProfilePic="user.profile_pic" />
    </header>
    <router-view @updateTitle="setTitle" />
  </div>
</template>


  
<script>
import axios from 'axios';
import { ref } from 'vue';
import ProfilePill from '@/components/ProfilePill.vue';

export default {
  components: {
    ProfilePill
  },
  data() {
    return {
      user: {
        name: '',
        email: '',
        profile_pic: '',
      },
      headerTitle: ref("Welcome to Betterave!")
    };
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/profile', { withCredentials: true });
      this.user = response.data;
    } catch (error) {
      console.error("There was an error fetching user data:", error);
    }
  },
  methods: {
    setTitle(newTitle) {
      this.headerTitle = newTitle;
    }
  }
};
</script>
  
<style>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  background-color: #f5f5f5; /* Background color for the square */
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1); /* subtle shadow for modern effect */
}

.betterave-logo {
  height: 70px; 
  width: auto;
  margin-left: 15px;

}

.ensae-logo {
  height: 150px;
  width: auto;
}

.logos-block {
  display: flex;
  align-items: center; /* This aligns children vertically in the middle */
}

h1 {
  font-size: 2rem;
  font-weight: 700; 
}

.fill-height {
  min-height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
</style>
  