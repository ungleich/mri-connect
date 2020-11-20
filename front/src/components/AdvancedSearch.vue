<template lang="pug">
.advanced-search
  b-tabs(v-model='activeTab')
    b-tab-item(label='Query Fields')
      //- p.search-tip
      //-   i Use the following fields and click Search for results.
      form(@submit.prevent='runSearch')
        .search-fields
          .card(v-for='(fld) in fields' :key='fld.name')
            .card-header
              p.card-header-title
                label.fld {{ fld.title }}
            .card-content
              .content
                input(type='text' v-model="fld.query")
                small.tip(v-show='fld.tip')
                  b-icon(icon='lightbulb' size='is-small' style='color:#0c0')
                  | {{ fld.tip }}

        b-button.search-button(type='is-primary'
            tag="input" native-type="submit"
            size='is-medium' value="Search")

    b-tab-item(label='Search Results' :visible='showResults')
      SearchResults(:advanced='searchQuery')
</template>

<script>
import $backend from '@/backend'
import SearchResults from '@/components/SearchResults.vue'

export default {
  name: 'AdvancedSearch',
  components: {
    SearchResults
  },
  data () {
    return {
      activeTab: 0,
      showResults: false,
      searchQuery: {},
      fields: [
        {
          'name': 'last_name__icontains',
          'title': 'Last Name',
          'tip': '"Muller" also finds "Müller"'
        },{
          'name': 'first_name__icontains',
          'title': 'First Name',
          'tip': '"Frank" also finds "Franklin"'
        },{
          'name': 'position__icontains',
          'title': 'Position'
        },{
          'name': 'official_functions__icontains',
          'title': 'Official functions'
        },{
          'name': 'list_publications__icontains',
          'title': 'Keywords in publications'
        // },{
        //   'name': 'affiliation.city',
        //   'title': 'City',
        //   'tip': 'enter City in local Language, e.g Genève, NOT Geneva'
        // },{
        //   'name': 'affiliation.country',
        //   'title': 'Country',
        //   'tip': 'in English (e.g. "Switzerland"), NOT in local language. England -&gt; Great Britain'
        }
      ]
    }
  },
  methods: {
    runSearch () {
      let self = this
      let query = {}
      Object.keys(this.fields).forEach((key) => {
        let fld = this.fields[key]
        if (typeof(fld.query) !== 'undefined' &&
            fld.query.length > 2) {
          query[fld.name] = fld.query
        }
      })
      if (Object.keys(query).length === 0) return;
      this.searchQuery = query
      this.activeTab = 1
      this.showResults = true
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.search-fields {
  max-height: 36em;
  overflow-y: auto;
  border-bottom: 1px solid #ccc;
  margin-bottom: 1em;

  input {
    font-size: 125%;
    margin-right: 1em;
  }
}
.search-tip {
  margin-top: 1em;
}
.content {
  text-align: left;
}
</style>
