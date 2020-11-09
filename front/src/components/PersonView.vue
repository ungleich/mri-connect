<template lang="pug">
.person-view
  p.card
    //- .fullname
    //-   | {{ person.title }}
    //-   | {{ person.first_name }}
    //-   | {{ person.last_name }}
    .photo
      img(:src="person.photo", height="100")
    .position
      | {{ person.position }}
    .career_stage
      | {{ person.career }}

  .institution
    b.name
      | {{ affiliation.name }}
    .department
      | {{ affiliation.department }}
    .address
      | {{ affiliation.street }}
    .city
      | {{ affiliation.postcode }}
      | {{ affiliation.city }}
    .country
      | {{ affiliation.country }}

  ul.personal_urls
    li(v-for="url in person.urls", v-bind:key="url")
      a(:href="url", target="_blank") {{ url }}

  .functions(v-show="person.official_functions")
    h5 Additional functions
    div {{ person.official_functions }}

  h5 Key publications
  .publications
    .item(v-for="res in person.resources")
      a(:href="res.url" target="_blank") {{ res.title }}
      .citation {{ res.citation }}
      .abstract {{ res.abstract }}
  //- h5 Expertise
  //- h5 Specialties
</template>

<script>
export default {
  name: 'PersonView',
  props: {
    person: Object
  },
  data () {
    return {
    }
  },
  watch: {

  },
  methods: {
  },
  mounted () {

  }
}
</script>

<style scoped lang="scss">
.person-view {
  text-align: left;
  margin: 1em;
}
.abstract {
  font-style: italic;
}
</style>
