import Vue from 'vue'
import Router from 'vue-router'

import Start from './views/Start.vue'
import Search from './views/Search.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'start',
      component: Start
    },
    {
      path: '/search',
      name: 'search',
      component: Search
    }
  ]
})
