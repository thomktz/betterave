<template>
  <v-container class="fill-height">
    <UserClassesTable
      :classes="classes"
      :available-classes.sync="availableClasses"
      :asAdmin="asAdmin"
      @request-classes="fetchClasses"
      @enroll-class="enrollInClass"
      @update-class-group="updateClassGroup"
      @delete-class="deleteClass"
    />
  </v-container>
</template>

<script>
import UserClassesTable from '@/components/UserClassesTable.vue';
import { apiClient, toast } from '@/apiConfig';


export default {
  components: {
    UserClassesTable
  },
  data () {
    return {
      user_id: this.$route.params.student_id,
      classesInfo: {},
      classes: [],
      availableClasses: [],
      name: '',
      surname: '',
      level: null,
      asAdmin: null,
    }
  },
  async mounted () {
    // Fetch the classes for the selected user
    const response = await apiClient.get(`/users/${this.user_id}/classgroups`);
    this.classesInfo = response.data;
    this.classes = this.classesInfo.classgroups;
    this.name = this.classesInfo.name;
    this.surname = this.classesInfo.surname;
    this.level = this.classesInfo.level;

    this.$emit('updateTitle', `${this.name} ${this.surname} Classes`);

    // Fetch the type of the current user (not the selected one!)
    const response2 = await apiClient.get(`/users/me`);
    this.asAdmin = (response2.data.user_type === 'admin');
  },
  methods: {
    async fetchClasses() {
      try {
        const response = await apiClient.get(`/classes/level/${this.level}`);
        const allAvailableClasses = response.data;

        // Filter out classes that are already enrolled
        this.availableClasses = allAvailableClasses.filter(availableClass => 
          !this.classes.some(enrolledClass => 
            enrolledClass.class_id === availableClass.class_id
          )
        );

      } catch (error) {
        console.error('Error fetching classes:', error);
      }
    },
    async enrollInClass(class_id) {
      try {

        // Perform the API call to enroll in the class
        const response = await apiClient.post(`/users/${this.user_id}/enroll/${class_id}`);
        // Add the class to the table
        this.classes.push(response.data);
        toast.success('Enrolled in class successfully')

      } catch (error) {
        console.error('Error enrolling in class:', error);
      }
    },
    async deleteClass(class_id) {
      try {

        // Perform the API call to delete the class
        const response = await apiClient.delete(`/users/${this.user_id}/unenroll/${class_id}`);

        // Remove the class from the table
        const classIndex = this.classes.findIndex(classItem => classItem.class_id === class_id);
        this.classes.splice(classIndex, 1);
        toast.success('Unenrolled from class successfully')

      } catch (error) {
        console.error('Error deleting class:', error);
      }
    },
    async updateClassGroup({ class_id, secondaryClassGroupName }) {
      try {
        // Perform the API call to update the UserClassGroup
        const update_data = {
          "secondary_class_group_name": secondaryClassGroupName
        }
        const response = await apiClient.put(`/user_class_groups/${this.user_id}/${class_id}`, update_data);
        
        // Handle the successful update
        toast.success('Class group updated successfully')
        // Optionally update local data to reflect the change
        
      } catch (error) {
        // Handle any errors
        console.error('Update failed:', error.response?.data || error.message);
      }
    },
  }

}
</script>

<style>

</style>