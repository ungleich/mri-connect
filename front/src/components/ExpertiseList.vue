<template lang="pug">
section.expertise-list
  b-collapse.card(animation='slide' v-for='topic in topics' :key='topic.id' :open='isOpen == index' @open='isOpen = index')
      .card-header(slot='trigger' slot-scope='props' role='button')
        p.card-header-title
          //- input(type='checkbox', :id='"t"+topic.id')
          label.topic(:for='"t"+topic.id') {{ topic.title }}
        a.card-header-icon
          b-icon(:icon="props.open ? 'menu-down' : 'menu-up'")
      .card-content
        .content(v-for='expertise in topic.expertise', v-bind:key='expertise.id')
          input(type='checkbox', :id='"e"+expertise.id')
          label.expertise(:for='"e"+expertise.id') {{ expertise.title }}
</template>

<script>
import $backend from '@/backend'

export default {
  name: 'ExpertiseList',
  components: {
  },
  props: {
  },
  data () {
    return {
      isOpen: 0,
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
          console.log(result)
          // Open result view
          self.topics = result
        })
        .catch((error) => console.error(error))
    }
  },
  mounted () {
    this.fetchTopics()
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
</style>
