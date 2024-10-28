import { createRouter, createWebHistory } from 'vue-router'
import DocCore from '../views/DocCore.vue'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/doc',
      name: 'doc',
      component: DocCore
    },
  ]
})

export default router
