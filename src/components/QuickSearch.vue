<template>
  <div class="search">
    <div class="quick-search">

      <h1>Find an expert</h1>
      <input v-model="query" placeholder="Quick search ...">

      <ul class="search-result" v-show="results.length > 0">
        <div>{{ results.length }} results</div>
        <li v-for="result in results" v-bind:key="result.id">
          {{ result.fullname }}
        </li>
      </ul>

    </div>

  </div>
</template>

<script>
import $backend from '@/backend'

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data () {
    return {
      query: '',
      results: []
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
.search-result li {
  display: block;
  border-top: 1px solid #999;
  padding: 1em;
}
.search-result div {
  padding: 1em;
  display: inline-block;
  width: auto;
  background: blue; color: white;
}
.search-result {
  border-bottom: 1px solid #999;
}
.quick-search input {
  font-size: 200%;
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
</style>
