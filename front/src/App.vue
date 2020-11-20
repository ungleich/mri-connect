<template>
  <div id="app">
    <AppHeader />
    <router-view/>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'

export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style lang="scss">
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
#app, .vs-popup, .vs-dialog {
  font-family: 'OpenSans', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  overflow-x: hidden;
  color: #5b5777;
}
.vs-popup {
  text-align: left;
}
.fullscreen .vs-popup header { display: none; }
.fullscreen .lightbox-container {
  height: 100%; padding: 10px 0 0; margin: 0px;
  .vs-button-text { color: black; text-shadow: 1px 1px 1px white; }
}
.vs-navbar--header > button.vs-navbar--btn-responsive { visibility: hidden; }

#app .vs-button-light { color: black; }
.together { white-space: nowrap; }

.vs-dialog .vs-dialog__close {
  top: 0px;
  right: 0px;
}
</style>
