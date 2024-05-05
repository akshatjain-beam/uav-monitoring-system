<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Home Page</h1>
    <div class="d-flex justify-content-center">
      <button class="btn btn-success mx-2" @click="goToHealth">Health</button>
      <button class="btn btn-primary mx-2" @click="goToTaskManagement">Task Management</button>
      <button class="btn btn-primary mx-2" @click="goToTaskDetails">Task Details</button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
  methods: {
    goToHealth() {
      this.$router.push({ name: 'Health' });
    },
    goToTaskManagement() {
      this.$router.push({ name: 'TaskManagement' });
    },
    goToTaskDetails() {
      this.$router.push({ name: 'TaskDetails' });
    },
  }
}
</script>
