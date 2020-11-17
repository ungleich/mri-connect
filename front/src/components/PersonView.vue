<template lang="pug">
.person-view
  .links
    b-button(outlined, :disabled="!person.url_personal", :href="person.url_personal")
      | Website
    b-button(outlined, :disabled="!person.url_cv", :href="person.url_cv")
      | CV
    b-button(outlined, :disabled="!person.url_researchgate", :href="person.url_researchgate")
      | ResearchGate
    b-button(outlined, :disabled="!person.url_publications", :href="person.url_publications")
      | Publications

  .card

    //- pre {{ person }}

    .photo(v-if="person.url_photo")
      img(:src="person.url_photo")

    .position
      | {{ person.position }}

    .topics
      .t(v-for="topic in person.topics")
        h5 {{ topic.title }}
        ul.expertise
          li(v-for="exp in topic.expertise")
            | {{ exp.title }}

    .affiliation(v-if="person.affiliation")
      h5 Affiliation
      .name
        | {{ person.affiliation.name }}
      .department
        | {{ person.affiliation.department }}
      .address
        | {{ person.affiliation.street }}
      .city
        | {{ person.affiliation.postcode }}
        | {{ person.affiliation.city }}
      .country
        | {{ person.affiliation.country }}

    .functions(v-show="person.official_functions")
      h5 Additional functions
      div {{ person.official_functions }}

    .career(v-show="person.career")
      h5 Career stage
      div {{ person.career }}
      div(v-show="person.career_graduation")
        .graduation Graduation year:
          span.date &nbsp;{{ person.career_graduation }}

    .publications(v-show="person.list_publications")
      h5 Key publications
      p(v-html="person.publications")

    //- h5 Expertise
    //- h5 Specialties

  .meta
    small Last updated:
      span.date &nbsp;{{ person.date_edited }}
  .update-me
    button.button.is-dark(@click='update_me')
      b-icon(icon='pencil')
      span Edit
</template>

<script>
export default {
  name: 'PersonView',
  props: {
    person: Object,
    topics: Array
  },
  data () {
    return {
    }
  },
  watch: {

  },
  methods: {
    update_me: function () {
      alert('Under construction ...')
    }
  },
  mounted () {

  }
}
</script>

<style scoped lang="scss">
.person-view {
  text-align: left;
  min-width: 34em;
  overflow-x: auto;
}
.card {
  margin: 2em 0em;
  padding: 1em;
}
.links {
  margin-bottom: 1em;
}
.abstract {
  font-style: italic;
}
.photo img {
  width: 140px;
  float: right;
  margin-left: 10px;
}
h5 {
  color: #aaa;
  margin: 0px;
  border-bottom: 1px solid #ddd;
  clear: both;
}
.meta {
  float: right;
  color: #999;
  margin: 0px;
}
.affiliation {
  .name {
    margin: 1em 0;
    font-weight: bold;
  }
  margin-bottom: 1em;
}
.publications > p {
  padding: 1em;
  background: #eee;
}
</style>
