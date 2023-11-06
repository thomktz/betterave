<template>
    <div>

    </div>
</template>

<script>
export default {
    data () {
      return {
        userId: this.$route.params.userId,
      }
    },
    async mounted () {
      response = await axios.get('/users', { withCredentials: true });
      this.$emit('updateTitle', ""); 
    },
}
</script>

<style>

</style>