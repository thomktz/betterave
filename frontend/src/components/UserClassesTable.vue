<template>
    <v-container>
      <!-- Classes Table -->
      <v-data-table
        :headers="headers"
        :items="classes"
        class="elevation-1"
      >
      <template v-slot:[`item.secondary_class_group_name`]="{ item }">
        <v-select
          :items="item.all_groups"
          v-model="item.secondary_class_group_name"
          @update:model-value="emitUpdateClass(item)"
          :label="getGroupName(item)"
          dense
        ></v-select>
      </template>
        
        <!-- Actions (Delete) -->
        <template v-slot:item.actions="{ item }">
          <v-icon
            small
            @click="emitDeleteClass(item.class_id)"
          >
            mdi-delete
          </v-icon>
        </template>
      </v-data-table>
    </v-container>
  </template>
  
  <script>
  export default {
    props: {
      classes: Array
    },
    data() {
      return {
        headers: [
          { title: 'Class Name', value: 'class_name' },
          { title: 'Secondary Group', value: 'secondary_class_group_name' },
          { title: '', value: 'actions', sortable: false }
        ],
      };
    },
    methods: {
      emitUpdateClass(item) {
        // Emit an event for the parent component to handle, passing the relevant data
        this.$emit('update-class-group', {
          classId: item.class_id,
          secondaryClassGroupName: item.secondary_class_group_name
        });
      },
      emitDeleteClass(classId) {
        console.log("Deleting class", classId);
        // this.$emit('delete-class', classId);
      },
      getGroupName(item) {
        return item.secondary_class_group_name ? "Secondary group" : 'No groups';
      },
    }
  };
  </script>
  
  <style scoped>
  .v-container {
    background-color: var(--secondary-color);
    color: var(--primary-text-color);
    padding: 0;
    margin-top: 20px;
    border-radius: 15px;
  }
  </style>