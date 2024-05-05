<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Task Details</h1>
    <div v-if="tasks.length === 0" class="text-muted">No tasks found</div>
    <div v-else>
      <!-- Refresh button -->
      <button @click="refreshData" class="btn btn-primary mb-3">Refresh</button>
      <table class="table">
        <!-- Table headers -->
        <thead>
          <tr>
            <th>Task Name</th>
            <th>Description</th>
            <th>Associated Drones</th>
            <th>Captured Images</th>
          </tr>
        </thead>
        <!-- Table body -->
        <tbody>
          <tr v-for="task in tasks" :key="task.id">
            <!-- Task details -->
            <td>{{ task.name }}</td>
            <td>{{ task.description }}</td>
            <td>{{ task.drone_name }}</td>
            <td>
              <!-- Image URLs -->
              <div v-if="!task.imageUrls.length" class="text-muted">
                No images captured
              </div>
              <div v-else>
                <ol>
                  <li v-for="(imageUrl, index) in task.imageUrls" :key="index">
                    {{ imageUrl }}
                  </li>
                </ol>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "TaskDetails",
  data() {
    return {
      tasks: [],
    };
  },
  mounted() {
    // Fetch initial data
    this.fetchTasks();
    // Start automatic data refresh every 5 minutes
    this.refreshInterval = setInterval(this.fetchTasks, 5 * 60 * 1000);
  },
  beforeDestroy() {
    // Clear refresh interval when component is destroyed
    clearInterval(this.refreshInterval);
  },
  methods: {
    async fetchTasks() {
      try {
        // Fetch tasks data from the API
        const response = await fetch("http://127.0.0.1:5000/api/tasks/");
        const tasksData = await response.json();
        console.log(tasksData); // Log the fetched tasks to console
        // Fetch image URLs for each task
        for (const task of tasksData) {
          const imageResponse = await fetch(
            `http://127.0.0.1:5000/api/tasks/${task.id}/images`
          );
          if (imageResponse.ok) {
            const imageData = await imageResponse.json();
            task.imageUrls = imageData.map((image) => image.url);
          } else {
            task.imageUrls = []; // Set empty array if no images or error occurred
          }
        }
        // Update tasks data
        this.tasks = tasksData;
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    },
    refreshData() {
      // Manually trigger data refresh when refresh button is clicked
      this.fetchTasks();
    },
  },
};
</script>

<style>
/* Add custom styles here */
</style>
