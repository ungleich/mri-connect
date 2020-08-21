<template>
  <div class="hello">
    <b style="text-transform: uppercase">Connect with the Mountain Research community</b>

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

    <h2>Advanced search</h2>
    <form action="#" style="text-align:center">
      <table border="0" cellspacing="0" cellpadding="2">
        <thead>
          <tr>
            <th><b>Input Field</b></th>
            <th><b>Search</b></th>
            <th><b>Example</b></th>
          </tr>
        </thead>
        <tbody>

          <tr>
            <td class="lvcol1" valign="top">Last Name</td>
            <td class="lvcol2" valign="top"><input type="text" name="2" value="" /></td>
            <td class="lvcol3" valign="top">&#39;Muller&#39; also finds &#39;Müller&#39;</td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">First Name</td>
            <td class="lvcol2" valign="top"><input type="text" name="3" value="" /></td>
            <td class="lvcol3" valign="top">&#39;Frank&#39; also finds &#39;Franklin&#39;</td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">Group / Unit</td>
            <td class="lvcol2" valign="top"><input type="text" name="46" value="" /></td>
            <td class="lvcol3" valign="top"></td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">Department / Institute</td>
            <td class="lvcol2" valign="top"><input type="text" name="6" value="" /></td>
            <td class="lvcol3" valign="top">&#39;@Biolog&#39; finds &#39;Institut de Biologie&#39;, &#39;Biological Department&#39; etc</td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">University / Company</td>
            <td class="lvcol2" valign="top"><input type="text" name="7" value="" /></td>
            <td class="lvcol3" valign="top">@Fribourg,  search is slow with WildCard @</td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">Street</td>
            <td class="lvcol2" valign="top"><input type="text" name="8" value="" /></td>
            <td class="lvcol3" valign="top"></td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">City</td>
            <td class="lvcol2" valign="top"><input type="text" name="10" value="" /></td>
            <td class="lvcol3" valign="top">enter City in local Language, e.g Genève, NOT Geneva</td>
          </tr>

          <tr>
            <td class="lvcol1" valign="top">Country Name</td>
            <td class="lvcol2" valign="top"><input type="text" name="12" value="" /></td>
            <td class="lvcol3" valign="top">in English (e.g. &#39;Switzerland&#39;), NOT in local language. England -&gt; Great Britain</td>
          </tr>

        </tbody>
      </table>
      <br/>
      <input type="hidden" name="w_Identifier" value="" />
      <input type="submit" value="find" style="
      line-height: 10px;
      border-width: 1px;
      padding: 5px 14px 5px;
      /* border-style: outset; */
      border-color: buttonface;
      border-image: initial;
      /* padding: 0; */
      margin: 0;
      font-family: &#39;Lato&#39;, sans-serif;
      font-size: 16px;
      line-height: 16px;
      background: #2d64d0;
      color: #fff;
      text-align: left;
      border-radius: 4px;
      font-size: 12px;
      font-style: normal;
      ">
    </form>

    <h3>Development</h3>
    <ul>
      <a href="https://github.com/vuejs/vue-cli/tree/dev/docs" target="_blank">vue-cli documentation</a>.
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel" target="_blank">babel</a></li>
      <li><a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-eslint" target="_blank">eslint</a></li>
      <li><a href="https://vuejs.org" target="_blank">Core Docs</a></li>
      <li><a href="https://forum.vuejs.org" target="_blank">Forum</a></li>
      <li><a href="https://chat.vuejs.org" target="_blank">Community Chat</a></li>
      <li><a href="https://twitter.com/vuejs" target="_blank">Twitter</a></li>
    </ul>
    <ul>
      <li><a href="https://router.vuejs.org/en/essentials/getting-started.html" target="_blank">vue-router</a></li>
      <li><a href="https://vuex.vuejs.org/en/intro.html" target="_blank">vuex</a></li>
      <li><a href="https://github.com/vuejs/vue-devtools#vue-devtools" target="_blank">vue-devtools</a></li>
      <li><a href="https://vue-loader.vuejs.org/en" target="_blank">vue-loader</a></li>
      <li><a href="https://github.com/vuejs/awesome-vue" target="_blank">awesome-vue</a></li>
    </ul>
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
