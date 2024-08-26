import { createRouter, createWebHistory } from 'vue-router'
import DocView from '../views/DocView.vue'
import DocCore from '../views/DocCore.vue'
// import DocCoreOld from '../views/DocCoreOld.vue'

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
      // component: DocCoreOld
    },
  ]
})

export default router
