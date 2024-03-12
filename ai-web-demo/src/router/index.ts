import { createRouter, createWebHistory } from 'vue-router'
import DocView from '../views/DocView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: DocView
    },
  ]
})

export default router
