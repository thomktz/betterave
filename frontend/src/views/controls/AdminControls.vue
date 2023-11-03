<template>
    <v-container class="fill-height" fluid>
        <UsersTable :users="usersList" @delete-user="deleteUser" />
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

        // Fetch the list of users on component mount
        onMounted(fetchUsers);

        return {
            usersList,
            deleteUser
        }
    }
}
</script>

<style>
/* Add your styles here */
</style>
