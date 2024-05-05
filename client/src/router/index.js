import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Health from '../components/Health.vue'
import TaskManagement from '../components/TaskManagement.vue'
import TaskDetails from '../components/TaskDetails.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/health',
      name: 'Health',
      component: Health
    },
    {
      path: '/taskManagement',
      name: 'TaskManagement',
      component: TaskManagement
    },
    {
      path: '/taskDetails',
      name: 'TaskDetails',
      component: TaskDetails
    },
  ]
})

export default router
