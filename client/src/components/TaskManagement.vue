<template>
  <div class="container">
    <h2>Task Management</h2>
    <div class="buttons">
      <button @click="openDialog('createTask')" class="button">
        Create Task
      </button>
      <button @click="openDialog('assignDrones')" class="button">
        Assign Drones
      </button>
      <button @click="openDialog('executeTask')" class="button">
        Execute Task
      </button>
    </div>

    <!-- Create Task Dialog -->
    <div v-if="dialogType === 'createTask'" class="dialog">
      <div class="popup-content">
        <span @click="closeDialog" class="close-button">×</span>
        <h3 class="form-heading">Create New Task</h3>
        <form @submit.prevent="createTask" class="form">
          <div class="form-group">
            <label for="taskName">Name:</label>
            <input
              type="text"
              id="taskName"
              v-model="taskName"
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="taskDroneId">Drone ID:</label>
            <input
              type="number"
              id="taskDroneId"
              v-model="taskDroneId"
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="description">Description:</label>
            <textarea
              id="description"
              v-model="description"
              class="input-field"
            ></textarea>
          </div>
          <button type="submit" class="submit-button">Create Task</button>
        </form>
      </div>
    </div>

    <!-- Assign Drones Dialog -->
    <div v-if="dialogType === 'assignDrones'" class="dialog">
      <div class="popup-content">
        <span @click="closeDialog" class="close-button">×</span>
        <h3 class="form-heading">Assign Drones to Task</h3>
        <form @submit.prevent="assignDrones" class="form">
          <div class="form-group">
            <label for="taskId">Task ID:</label>
            <input
              type="text"
              id="taskId"
              v-model="taskId"
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="drones">Drones:</label>
            <input
              type="text"
              id="drones"
              v-model="drones"
              class="input-field"
            />
          </div>
          <button type="submit" class="submit-button">Assign Drones</button>
        </form>
      </div>
    </div>

    <!-- Execute Task Dialog -->
    <div v-if="dialogType === 'executeTask'" class="dialog">
      <div class="popup-content">
        <span @click="closeDialog" class="close-button">×</span>
        <h3 class="form-heading">Execute Task</h3>
        <form @submit.prevent="executeTask" class="form">
          <div class="form-group">
            <label for="executeTaskId">Task ID:</label>
            <input
              type="text"
              id="executeTaskId"
              v-model="executeTaskId"
              class="input-field"
            />
          </div>
          <button type="submit" class="submit-button">Execute Task</button>
        </form>
      </div>
    </div>

    <!-- Response from Backend -->
    <div v-if="response" class="response">
      <span @click="closeResponse" class="close-button">×</span>
      <p>{{ response }}</p>
    </div>
  </div>
</template>

<script>

export default {
  name: "TaskManagement",
  data() {
    return {
      dialogType: "",
      taskName: "",
      taskDroneId: "",
      description: "",
      taskId: "",
      drones: "",
      executeTaskId: "",
      response: "",
    };
  },
  methods: {
    openDialog(type) {
      this.dialogType = type;
    },
    closeDialog() {
      this.dialogType = "";
    },
    closeResponse() {
      this.response = "";
    },
    createTask() {
      const path = "http://127.0.0.1:5000/api/tasks/";
      const data = {
        name: this.taskName,
        drone_id: this.taskDroneId,
        description: this.description,
      };

      fetch(path, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.response = data;
        })
        .catch((error) => {
          console.error("Error:", error);
          this.response = "Error: Unable to create task.";
        });

      this.taskName = "";
      this.taskDroneId = "";
      this.description = "";
      this.dialogType = "";
    },

    assignDrones() {
      const path = `http://127.0.0.1:5000/api/tasks/${this.taskId}`;
      const data = {
        drone_id: this.drones,
      };

      fetch(path, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.response = data;
        })
        .catch((error) => {
          console.error("Error:", error);
          this.response = "Error: Unable to assign drones to task.";
        });

      this.taskId = "";
      this.drones = "";
      this.dialogType = "";
    },

    executeTask() {
      const path = `http://127.0.0.1:5000/api/tasks/${this.executeTaskId}/execute`;

      fetch(path, {
        method: "POST",
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          this.response = data;
        })
        .catch((error) => {
          console.error("Error:", error);
          this.response = "Error: Unable to execute task.";
        });

      this.executeTaskId = "";
      this.dialogType = "";
    },
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 20px;
}

.buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: left;
}

.popup-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  position: relative;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}

.input-field {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.response {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #aaa;
  padding: 20px;
  border-radius: 5px;
  z-index: 9999;
}

.popup-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-heading {
  margin-bottom: 20px;
}

.form {
  width: 100%;
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.form-group label {
  width: 100px; /* Adjust width as needed */
  margin-right: 10px;
}

.input-field {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-button {
  width: fit-content;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>
