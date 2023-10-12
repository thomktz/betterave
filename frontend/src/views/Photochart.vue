<template>
    <div>
      <h1 class="page-title">Trombinoscope</h1>
      <div class="custom-select"> <!-- Ajout d'une classe pour personnaliser la barre déroulante -->
        <select v-model="selectedClass">
          <option value="all">Toutes les classes</option>
          <option v-for="cls in classes" :value="cls">{{ cls }}</option>
        </select>
      </div>
  
      <div class="trombinoscope">
        <div v-for="user in filteredTrombinoscope" :key="user.id" class="user">
          <img :src="user.profile_pic" :alt="user.name" />
          <p>{{ user.name }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import ProfilePill from '@/components/ProfilePill.vue';

  export default {
    components: {
    ProfilePill,
  },
    data() {
      return {
      user: {
        name: '',
        email: '',
        level: ''
      },
        classes: ['1A', '2A', '3A'], // Liste des classes
        selectedClass: 'all', // Classe sélectionnée dans la barre déroulante

    };
},
    computed: {
      filteredTrombinoscope() {
        if (this.selectedClass === 'all') {
          return this.trombinoscope;
        } else {
          return this.trombinoscope.filter((user) => user.class === this.selectedClass);
        }
      },
    },
    async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/photochart', { withCredentials: true });
      this.user = response.data;
    } catch (error) {
      console.error("There was an error fetching user data:", error);
    }
  },
  methods: {
  }
  }

  
  </script>
  
  <style scoped>
  .page-title {
    text-align: center; /* Pour centrer le titre */
    background-color: #a3cdcf; /* Couleur de fond */
    color: white; /* Couleur du texte */
    padding: 20px; /* Espace intérieur */
  }
  
  .custom-select {
  text-align: center;
  margin-top: 20px;
  position: relative; /* Permet de positionner les éléments fils */
}

.custom-select select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  appearance: none; /* Supprime le style par défaut du navigateur */
  -webkit-appearance: none; /* Pour les navigateurs WebKit */
  -moz-appearance: none; /* Pour les navigateurs basés sur Gecko */
  background-color: #f2f2f2;
  color: #333;
  cursor: pointer;
}

/* Style de survol du curseur */
.custom-select select:hover {
  background-color: #e0e0e0;
}
  .trombinoscope {
    display: flex;
    flex-wrap: wrap;
  }
  
  .select-container {
  text-align: center; /* Pour centrer la barre déroulante horizontalement */
  margin-bottom: 20px; /* Pour ajouter de l'espace en bas de la barre déroulante */
}

  .person {
    margin: 10px;
    text-align: center;
  }
  
  img {
    max-width: 200px;
    max-height: 200px;
  }
  </style>
    