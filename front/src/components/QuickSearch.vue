<template lang="pug">
.search
  .quick-search
    input(v-model='query', placeholder='Quick search ...')
  template
    .search-result
      vs-table(v-show='results.length > 0')
        template(#thead)
          vs-tr
            vs-th Last name
            vs-th First name
            vs-th Location
            vs-th Details
        template(#tbody)
          vs-tr(v-for='result in results', v-bind:key='result.id', :data='result')
            vs-td
              .last_name {{ result.last_name }}
            vs-td
              .first_name {{ result.first_name }}
            vs-td
              .location {{ result.location }}
            vs-td
              vs-button(flat, icon, @click="selectItem(result.id)")
                box-icon(name='expand-alt')
                | Open
            //template(#expand)
              .con-content
                .left
                  vs-avatar
                    img(:src="result.url_image")
                  span {{ result.fullname }}
                .right
                  vs-button(flat, icon, @click="selectItem(result.id)")
                    box-icon(name='expand-alt')
                    | Open
        template(#footer).summary
          | {{ counts }} results

  vs-dialog(v-model='popup')
    template(#header='')
      .not-margin.person-title
        | {{ selectedPerson.fullname }}
    PersonView(:person='selectedPerson')
    template(#footer='')
      .footer-dialog
        vs-button(block, gradient, size='large', @click='popup=false') Close
</template>

<script>
import $backend from '@/backend'
import PersonView from '@/components/PersonView.vue'

export default {
  name: 'QuickSearch',
  components: {
    PersonView
  },
  props: {
    msg: String
  },
  data () {
    return {
      query: '',
      nextpage: null,
      results: [],
      counts: 0,
      popup: false,
      selectedPerson: {}
    }
  },
  watch: {
    query (val) { this.runQuery(val) }
  },
  methods: {
    selectItem (pid) {
      let self = this
      $backend.getPeopleData(pid)
        .then(responseData => {
          let result = {}
          // Map keyed results
          Object.keys(responseData).forEach((key) => {
            result[key] = responseData[key]
          })
          // Open result view
          self.selectedPerson = result
          self.popup = true
        })
        .catch((error) => console.error(error))
    },
    runQuery (val) {
      let self = this
      if (val.length < 3) return
      $backend.getPeopleSearch(val)
        .then(responseData => {
          self.nextpage = responseData['next']
          self.results = responseData['results']
          self.counts = responseData['count']
        })
        // .catch((error) => this.promptNetworkError(error))
    }
  },
  mounted () {
    // Default search
    this.runQuery('latest')
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.quick-search {
  input {
    font-size: 200%;
  }
}
</style>
