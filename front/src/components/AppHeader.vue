<template lang="pug">
  b-navbar.header
    template(slot='start')
      b-navbar-item(tag='router-link' :to="{ path: '/search' }")
        | Find An Expert
      b-navbar-item(tag='router-link' :to="{ path: '/advanced' }")
        |  Advanced Search
      b-navbar-item(tag='router-link' :to="{ path: '/expertise' }")
        |  Search by Expertise
</template>

<script>
export default {
  name: 'AppHeader',
  props: {
  }
}
</script>

<style scoped lang="scss">
.header {
  margin-bottom: 80px;
}

button { margin: 0; padding: 0; }

nav {
  background: black;
}

a.navbar-item {
  color: #66a4d1;
  background: #000;
  text-decoration: none;
  padding: 20px 25px;
  font-family: 'Lato', sans-serif;
  font-weight: 400;
  font-size: 20px;
  text-decoration: none;
  u {
    border-bottom: 2px solid blue;
  }
  &.router-link-exact-active, &:hover {
    color: #fff;
    background: #0067b2;
  }
}
</style>
