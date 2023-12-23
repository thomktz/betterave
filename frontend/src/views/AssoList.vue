<template>
  <v-container class="fill-height" fluid>
    <div class="content-container">
      <div class="asso-list-container">
        <ul v-if="assos.length">
          <li
            v-for="asso in assos"
            :key="asso.user_id"
            @click="toggleSubscription(asso)"
            :class="asso.subscribed ? 'subscribed' : ''"
          >
            <img
              :src="'/' + asso.profile_pic"
              alt="Asso Logo"
              class="asso-logo"
            />
            <span class="asso-name">{{ asso.name }}</span>
            <div v-if="asso.subscribed" class="tick-mark">✓</div>
          </li>
        </ul>
        <div v-else>Loading associations...</div>
      </div>
    </div>
  </v-container>
</template>

<script>
import { apiClient } from "@/apiConfig";

export default {
  data() {
    return {
      assos: [],
    };
  },
  async mounted() {
    this.$emit("updateTitle", "Association subscriptions");
    try {
      const response = await apiClient.get("/users/associations/me");
      this.assos = response.data;
    } catch (error) {
      console.error("There was an error fetching associations data:", error);
    }
  },
  methods: {
    async toggleSubscription(asso) {
      asso.subscribed = !asso.subscribed;
      try {
        if (asso.subscribed) {
          await apiClient.post(`/users/me/subscribe/${asso.user_id}`);
        } else {
          await apiClient.delete(`/users/me/unsubscribe/${asso.user_id}`);
        }
      } catch (error) {
        console.error("There was an error toggling subscription:", error);
        // If an error occurs, revert checkbox to its previous state
        asso.subscribed = !asso.subscribed;
      }
    },
  },
};
</script>

<style scoped>
.asso-list-container {
  background-color: var(--foreground-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 70%;
  max-height: 80vh;
  overflow-y: auto;
  margin: auto;
}

.content-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
  width: 100%;
}

li {
  display: flex;
  align-items: center;
  height: 70px;
  border-bottom: 1px solid #b0b0b0;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

li:hover {
  background-color: rgba(123, 123, 123, 0.4);
}

.subscribed {
  background-color: rgba(25, 0, 255, 0.1);
}

.asso-logo {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 20px;
}

.asso-name {
  flex-grow: 1;
}

.tick-mark {
  font-size: 1.5em;
  color: green;
  margin-left: 20px;
}
</style>
