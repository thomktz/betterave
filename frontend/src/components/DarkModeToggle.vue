<template>
  <div @click="toggle" class="dark-mode-toggle">
    <span v-if="darkMode">🌙</span>
    <span v-else>☀️</span>
  </div>
</template>
  
  <script>
  export default {
    props: {
      darkMode: {
        type: Boolean,
        required: true,
      },
    },
    methods: {
      toggle() {
        this.$emit('toggle');
      },
    },
  };
  </script>
  
  <style scoped>
.dark-mode-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%; /* makes it circular */
  background-color: #686868;
  width: 50px;
  height: 50px;
  cursor: pointer;
}
  </style>
  