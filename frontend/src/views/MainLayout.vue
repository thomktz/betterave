<template>
  <div>
    <header class="header">

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

      <div class="right-section">
        <ProfilePill :userEmail="user.email" :userProfilePic="user.profile_pic" />
        <DarkModeToggle @toggle="toggleDarkMode" :darkMode="darkMode" />
      </div>

    </header>
    <router-view @updateTitle="setTitle" />
  </div>
</template>


  
<script>
import axios from 'axios';
import { ref } from 'vue';
import ProfilePill from '@/components/ProfilePill.vue';
import DarkModeToggle from '@/components/DarkModeToggle.vue';

export default {
  components: {
    ProfilePill,
    DarkModeToggle,
  },
  data() {
    return {
      user: {
        name: '',
        email: '',
        profile_pic: '',
      },
      headerTitle: ref("Welcome to Betterave!"),
      darkMode: false
    };
  },
  async mounted() {
    const storedPreference = localStorage.getItem('darkMode');
    if (storedPreference !== null) {
      this.darkMode = storedPreference === 'true';
    } else {
      this.darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    document.documentElement.setAttribute('data-dark-mode', this.darkMode);
    try {
      const response = await axios.get('/profile', { withCredentials: true });
      this.user = response.data;
    } catch (error) {
      console.error("There was an error fetching user data:", error);
    }
  },
  methods: {
    setTitle(newTitle) {
      this.headerTitle = newTitle;
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      document.documentElement.setAttribute('data-dark-mode', this.darkMode);
      localStorage.setItem('darkMode', this.darkMode); 
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
  background-color: var(--foreground-color);
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

.right-section {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-right: 20px;
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
  