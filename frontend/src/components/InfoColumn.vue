<template>
    <div class="info-column">
      <h2>{{ title }}</h2>
      <ul>
        <li v-for="item in list" :key="item.id">{{ item.text }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: {
        type: String,
        required: true
      },
      list: {
        type: Array,
        default: () => []
      }
    }
  }
  </script>
  
  <style scoped>
  .info-column {
    flex: 1;
    padding: 20px;
    background-color: #f5f5f5;
    border-radius: 10px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    margin: 0 10px;
  }
  
  h2 {
    font-size: 1.5rem;
    margin-bottom: 20px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin-bottom: 10px;
  }
  </style>
  