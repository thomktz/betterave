<template>
  <div class="info-column">
    <h2>{{ title }}</h2>
    <ul>
      <li v-for="item in list" :key="item.id">
        <div :style="getEventStyle(item)" class="event-item">
          {{ (item.text, item.start) }}
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    list: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    getEventStyle(item) {
      return {
        backgroundColor: item.color || "#4868bf", // If color is not provided, use a default color (#FFD700 is golden)
      };
    },
  },
};
</script>

<style scoped>
.info-column {
  flex: 1;
  padding: 20px;
  background-color: var(--secondary-color);
  color: var(--primary-text-color);
  border-radius: 10px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
  margin: 0 10px;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  border-bottom: 1px solid #b0b0b0;
  padding-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

.event-item {
  padding: 10px;
  border-radius: 10px;
  color: white;
}
</style>
