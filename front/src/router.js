import Vue from 'vue'
import Router from 'vue-router'

import Search from './views/Search.vue'
import Advanced from './views/Advanced.vue'
import Expertise from './views/Expertise.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/search',
      name: 'search',
      component: Search
    },
    {
      path: '/advanced',
      name: 'advanced',
      component: Advanced
    },
    {
      path: '/expertise',
      name: 'expertise',
      component: Expertise
    }
  ]
})
