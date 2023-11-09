<template>
  <div class="fill-height">
    <UserClassesTable :classes="classes" @update-class-group="updateClassGroup"></UserClassesTable>
  </div>
</template>

<script>
import UserClassesTable from '@/components/UserClassesTable.vue';
import apiClient from '@/apiConfig';

export default {
  components: {
    UserClassesTable
  },
  data () {
    return {
      userId: this.$route.params.student_id,
      classesInfo: {},
      classes: [],
      name: '',
      surname: '',
    }
  },
  async mounted () {
    const response = await apiClient.get(`/users/${this.userId}/classgroups`);
    console.log(response.data);
    this.classesInfo = response.data;
    this.classes = this.classesInfo.classgroups;
    this.name = this.classesInfo.name;
    this.surname = this.classesInfo.surname;

    console.log(this.classes);
    this.$emit('updateTitle', `${this.name} ${this.surname} Classes`);
  },
  methods: {
    async updateClassGroup({ classId, secondaryClassGroupName }) {
      try {
        // Perform the API call to update the UserClassGroup
        console.log(classId, secondaryClassGroupName)
        const update_data = {
          "secondary_class_group_name": secondaryClassGroupName
        }
        const response = await apiClient.put(`/user_class_groups/${this.userId}/${classId}`, update_data);
        
        // Handle the successful update
        console.log('Update successful:', response.data);
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