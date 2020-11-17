<template lang="pug">
.expertise-list
  vs-collapse.topics
    vs-collapse-item(v-for='topic in topics', v-bind:key='topic.id')
      .t(slot="header")
        input(type='checkbox', :id='"t"+topic.id')
        label.topic(:for='"t"+topic.id') {{ topic.title }}
      .e(v-for='expertise in topic.expertise', v-bind:key='expertise.id')
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
.topics {
  text-align: left;
}
.expertise-list {
  margin-left: 25%;
}
.t, .e {
  margin: 1em;
}
.t {
  margin-bottom: 2em;
}
.topic {
  font-weight: bold;
}
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
