<template>
    <v-container class="fill-height" fluid>
        <UsersTable
          :users="usersList"
          @delete-user="deleteUser"
          @add-user="addUser"
          @edit-user="editUser"
        />
    </v-container>
</template>

<script>
import axios from 'axios';
import UsersTable from '@/components/UsersTable.vue';
import { ref, onMounted } from 'vue';

export default {
    components: {
        UsersTable
    },
    mounted () {
      this.$emit('updateTitle', "Admin Controls"); 
    },
    setup() {
        const usersList = ref([]); // Create a reactive reference for the users list

        // Fetch users from the API
        const fetchUsers = async () => {
            try {
                const response = await axios.get('/users', { withCredentials: true });
                usersList.value = response.data; // Assign the response data to usersList
            } catch (error) {
                console.error('Error fetching users:', error);
                // Handle error, e.g., show notification
            }
        };

        // Delete user by ID
        const deleteUser = async (userId) => {
            try {
                await axios.delete(`/users/${userId}`, { withCredentials: true });
                // Upon successful deletion, refetch the users list or remove the user from the local list
                usersList.value = usersList.value.filter(user => user.id !== userId);
                // Show success notification
                
            } catch (error) {
                console.error('Error deleting user:', error);
                // Handle error, e.g., show notification
            }
        };
        // Add a new user
        const addUser = async (userData) => {
            try {
                const response = await axios.post('/users', userData, { withCredentials: true });
                usersList.value.push(response.data); // Add the new user to the list
                // Show success notification
            } catch (error) {
                console.error('Error adding user:', error);
                // Handle error, e.g., show notification
            }
        };

        // Edit existing user details
        const editUser = async (userData) => {
            try {
                await axios.put(`/users/${userData.id}`, userData, { withCredentials: true });
                // Find and update the user in the list
                const index = usersList.value.findIndex(user => user.id === userData.id);
                if (index !== -1) {
                    usersList.value[index] = {...usersList.value[index], ...userData};
                }
                // Show success notification
            } catch (error) {
                console.error('Error editing user:', error);
                // Handle error, e.g., show notification
            }
        };

        onMounted(fetchUsers);
        return {
            usersList,
            deleteUser,
            addUser,
            editUser
        }
    }
}
</script>

<style>
/* Add your styles here */
</style>
