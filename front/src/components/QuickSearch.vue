<template lang="pug">
.search
  .quick-search
    input(v-model='query', placeholder='Quick search ...')
  section
    .search-result
      b-table(
        :data='results'
        :columns='columns'
        :selected.sync="selected"
        @click="popup = true"
        focusable
        v-show='results.length > 0'
        style='width:auto'
      )
      template(slot='footer')
        .summary
          | {{ counts }} results

  b-modal(
    :active.sync='popup'
    has-modal-card
    trap-focus
    :destroy-on-hide='false'
    aria-role='dialog'
    aria-modal
  )
    .modal-card(style='width: auto')
      header.modal-card-head
        p.modal-card-title
          | {{ selected.fullname }}
      section.modal-card-body
        PersonView(:person='selectedPerson')
      footer.modal-card-foot
        button.button(type='button' @click='popup=false') Close
        button.button(type='button' @click='updateme=true')
          b-icon(icon='pencil')
          span Update

  b-modal(
    :active.sync='updateme'
    has-modal-card
    trap-focus
    :destroy-on-hide='false'
    aria-role='dialog'
    aria-modal
  )
    .modal-card(style='width: auto')
      header.modal-card-head
        p.modal-card-title
          | Update profile
      section.modal-card-body
        p Option 1) Self-service
        button.button(type='button' @click='requestAccess')
          span I am this person and would like to receive access to update my profile
        hr
        p Option 2) Recommend corrections
        textarea.corrections
        button.button(type='button' @click='requestAccess')
          span Send this note to the MRI administration
      footer.modal-card-foot
        button.button(type='button' @click='updateme=false') Close
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
      updateme: false,
      selected: {},
      selectedPerson: {},
      columns: [
        { 'field': 'last_name', 'label': 'Last name' },
        { 'field': 'first_name', 'label': 'First name' },
        { 'field': 'location', 'label': 'Location' }
      ]
    }
  },
  watch: {
    query (val) { this.runQuery(val) },
    selected (val) { this.selectItem(val.id) }
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
    },
    requestAccess () {
      this.updateme = false
      alert('You should receive an e-mail shortly. If you do not within 1 hour, please contact us at info@mountainresearch.org')
    }
  },
  mounted () {
    // Default search
    this.runQuery('latest')
  }
}
</script>

<style lang="scss">
.quick-search {
  input {
    font-size: 200%;
  }
}
.search-result {
  padding: 0 1em;
  text-align: center;
  .b-table .table { width: auto; }
}
@media (min-width: 1000px) {
  .search-result {
    padding: 0 10%;
  }
}
.corrections {
  width:100%; height:4em;
  padding: 0.5em 1em;
  font-size: 125%;
}
</style>
