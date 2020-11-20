<template lang="pug">
.expertise-list
  b-tabs(v-model='activeTab')
    b-tab-item(label='Expertise Selection')
      b-button.search-button(type='is-primary' size='is-medium'
          :disabled='selectExpertise.length == 0' @click='runSearch')
        b-icon(icon='magnify')
        span Search
      p.search-tip
        i Select one or more kinds of expertise below, and click Search for results.
      b-collapse.card(
            animation='slide' v-for='(topic, index) in topics'
            :key='topic.id' :open='isOpen == index' @open='isOpen = index')
        .card-header(slot='trigger' slot-scope='props' role='button')
          p.card-header-title
            | {{ parseInt(index) + 1 }}
            //- input(type='checkbox', :id='"t"+topic.id')
            label.topic(:for='"t"+topic.id') {{ topic.title }}
          a.card-header-icon
            b-icon(:icon="props.open ? 'menu-down' : 'menu-up'")
        .card-content
          .content(v-for='expertise in topic.expertise', v-bind:key='expertise.id')
            input(type='checkbox' :id='"e"+expertise.id' v-model="selectExpertise" :value='expertise.id')
            label.expertise(:for='"e"+expertise.id') {{ expertise.title }}

    b-tab-item(label='Search Results' :visible='selection.length > 0')
      SearchResults(:expertise='selection')
</template>

<script>
import $backend from '@/backend'
import SearchResults from '@/components/SearchResults.vue'

export default {
  name: 'ExpertiseList',
  components: {
    SearchResults
  },
  data () {
    return {
      selectExpertise: [],
      selection: [],
      activeTab: 0,
      isOpen: -1,
      topics: []
    }
  },
  methods: {
    fetchTopics () {
      let self = this
      $backend.getExpertiseTopics()
        .then(responseData => {
          let result = {}
          // Map keyed results
          Object.keys(responseData).forEach((key) => {
            result[key] = responseData[key]
          })
          // console.log(result)
          // Open result view
          self.topics = result
        })
        .catch((error) => console.error(error))
    },
    runSearch () {
      if (this.selectExpertise.length === 0) return
      this.selection = Array.from(this.selectExpertise.values())
      // console.log(this.selection);
      this.activeTab = 1
    }
  },
  mounted () {
    // TODO: caching
    if (this.topics.length === 0) {
      this.fetchTopics()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
input {
  transform: scale(1.5);
}
label {
  padding-left: 1em;
  cursor: pointer;
  &:hover {
    text-shadow: 3px 3px 3px yellow;
  }
}
.search-tip {
  margin-top: 1em;
}
.content {
  text-align: left;
}
</style>
