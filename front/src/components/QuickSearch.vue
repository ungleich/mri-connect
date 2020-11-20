<template lang="pug">
.search
  .quick-search
    input(v-model='query', placeholder='Quick search ...')
    button.button(type='button')
      b-icon(icon='magnify')
      span Go
  section
    SearchResults(:query='query' recent)
</template>

<script>
import SearchResults from '@/components/SearchResults.vue'

export default {
  name: 'QuickSearch',
  components: {
    SearchResults
  },
  data () {
    return {
      query: ''
    }
  }
}
</script>

<style lang="scss">
.quick-search {
  input {
    font-size: 180%;
  }
  button {
    margin-left: 1em;
  }
}
</style>
