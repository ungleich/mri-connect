<template lang="pug">
.search
  .quick-search
    h1 Find an expert
    input(v-model='query', placeholder='Quick search ...')
  .search-result
    table(v-show='results.length > 0')
      thead
        tr
          td Last name
          td First name
          td City
          td Country
      tbody
        tr(v-for='result in results', v-bind:key='result.id', @click="selectItem(result)")
          td
            .last_name {{ result.last_name }}
          td
            .first_name {{ result.first_name }}
          td
            .city {{ result.city }}
          td
            .country {{ result.country }}
      .summary
        | {{ results.length }} results
  vs-dialog(v-model='popup')
    template(#header='')
      h4.not-margin
        | {{ selectedPerson.fullname }}
    PersonView(:person='selectedPerson')
    template(#footer='')
      .footer-dialog
        vs-button.update-btn(flat='', size='small', color='info', type='border', style='float:right') Update this data
        vs-button.back-btn(flat='', size='large', color='dark', type='border', @click='popup=false') Close
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
      results: [],
      popup: false,
      selectedPerson: {}
    }
  },
  watch: {
    query: function (val) {
      if (val.length > 2) {
        $backend.getPeopleSearch(val)
          .then(responseData => {
            this.results = responseData
          })
          // .catch((error) => this.promptNetworkError(error))
      }
    }
  },
  methods: {
    selectItem (result) {
      let self = this
      $backend.getPeopleData(result.id)
        .then(responseData => {
          Object.keys(responseData).forEach((key) => {
            result[key] = responseData[key]
          })
          console.log(result)
          self.selectedPerson = result
          self.popup = true
        })
        .catch((error) => console.error(error))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h1, h2 {
  margin: 1em;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
form * {
  text-align: left;
  padding: 5px;
}
form {
  margin: 0 10%;
}
a {
  color: #42b983;
}

.quick-search {
  input {
    font-size: 200%;
  }
}

.search-result {
  text-align: center;
  margin-top: 3em;

  ul {
    border-bottom: 1px solid #999;
    li {
      display: block;
      border-top: 1px solid #999;
      padding: 1em;
      div {
        padding: 1em;
        display: inline-block;
        width: auto;
        background: blue; color: white;
      }
    }
  }

  table {
    display: inline-block;
    text-align: left;
    min-width: 560px;
    border-spacing: 0px;

    thead td {
      border-bottom: 2px solid #999;
      background-color: #eee;
      vertical-align: bottom;
    }
    tbody tr:hover {
      background-color: #d6e4f1;
      td { color: blue; cursor: pointer; }
    }
    th, td {
      padding: 10px;
      margin: 0px;
      border: 0px;
      text-align: left;
    }
    td {
      border-bottom: 1px solid #ccc;
      width: 15%;
    }
    td:first-child {
      width: 30%;
    }
    .summary {
      margin-top: 1em;
      text-align: center;
      font-size: 125%;
    }
  }
}
</style>
