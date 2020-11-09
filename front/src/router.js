import Vue from 'vue'
import Router from 'vue-router'

import Start from './views/Start.vue'
import Search from './views/Search.vue'
import Expertise from './views/Expertise.vue'

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
    },
    {
      path: '/expertise',
      name: 'expertise',
      component: Expertise
    }
  ]
})
