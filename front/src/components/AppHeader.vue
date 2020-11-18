<template lang="pug">
  .header
    router-link.item(:to="{ path: '/search' }")
      | Find An Expert
    router-link.item(:to="{ path: '/advanced' }")
      |  Advanced Search
    router-link.item(:to="{ path: '/expertise' }")
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
  background: black;
  margin-bottom: 80px;
  min-height: 3.25rem;
  position: relative;
  z-index: 30;
  text-align: center;
}

button { margin: 0; padding: 0; }

a.item {
  display: inline-block;
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
