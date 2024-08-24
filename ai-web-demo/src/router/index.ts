import { createRouter, createWebHistory } from 'vue-router'
import DocView from '../views/DocView.vue'
import DocCore from '../views/DocCore.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: DocView
    },
    {
      path: '/doc',
      name: 'doc',
      component: DocCore
    },
  ]
})

export default router
