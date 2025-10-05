import { createRouter, createWebHistory } from 'vue-router'
import Profile from '../views/Profile.vue'
import Diet from '../views/Diet.vue'

const routes = [
  { path: '/', redirect: '/profile' },
  { path: '/diet', component: Diet },
  { path: '/profile', component: Profile },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router