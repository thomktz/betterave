<template>
    <div class="users-table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>Profile Pic</th>
            <th>Surname</th>
            <th>Name</th>
            <th>Level</th>
            <th>Type</th>
            <th>Email</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>
              <img :src="'/' + user.profile_pic" class="profile-pic" alt="user.name"/>
            </td>
            <td>{{ user.surname }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.level }}</td>
            <td>{{ user.user_type }}</td>
            <td>{{ user.email }}</td>
            <td>
                <button @click="emitDeleteUser(user.id)" class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UsersTable',
    props: {
      users: Array
    },
    methods: {
      emitDeleteUser(userId) {
        // Emit an event to the parent component
        this.$emit('delete-user', userId);
      }
    }
  }
  </script>
  
  <style scoped>
  .users-table-container {
    overflow-x: auto;
  }
  
  .users-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }
  
  .users-table th,
  .users-table td {
    text-align: left;
    padding: 12px;
    border-bottom: 1px solid #ddd;
  }
  
  .users-table th {
    background-color: #f4f4f4;
  }
  
  .profile-pic {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .delete-btn {
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    background-color: #ff4d4f;
    color: white;
    cursor: pointer;
  }
  
  .delete-btn:hover {
    background-color: #ff7875;
  }
  </style>
  