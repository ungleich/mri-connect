<template lang="pug">
.search
  .quick-search
    h1 Find an expert
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
    PersonView(:person='selectedPerson', :topics='topics')
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
      topics: null,
      topiclookup: null,
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
          Object.keys(responseData).forEach((key) => {
            result[key] = responseData[key]
          })
          // console.log(result)
          self.topics = []
          result.expertise.forEach((e) => {
            topic = {
              'id': e.topic.id,
              'title': self.topiclookup[e.topic.id]
            }
            if (self.topics.indexOf(topic)<0)
              self.topics.push(topic)
          })
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
    fetchTopics () {
      let self = this
      return $backend.getExpertiseTopics()
        .then(responseData => {
          self.topiclookup = {}
          responseData.forEach((t) => {
            self.topiclookup[t.id] = t.title
          })
        })
        .catch((error) => alert(error))
    }
  },
  mounted () {
    let self = this
    this.fetchTopics().then(() => {
      self.runQuery('latest')
    })
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

.person-title {
  font-size: 140%;
  font-weight: bolder;
  color: #0067b2;
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
