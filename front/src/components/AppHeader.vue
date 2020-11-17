<template>
  <div class="header">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >
      <vs-navbar-item>
        <router-link to="/">
          Find An Expert
        </router-link>
      </vs-navbar-item>
      <vs-navbar-item disabled>
        <router-link to="#advanced">
          Advanced Search
        </router-link>
      </vs-navbar-item>
      <vs-navbar-item>
        <router-link to="/expertise">
          Search by Expertise
        </router-link>
      </vs-navbar-item>
    </vs-navbar>
  </div>
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

.vs-navbar--title {
  img {
    height: 80px;
  }
}

button { margin: 0; padding: 0; }

a {
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
  &.router-link-exact-active {
    color: #fff;
    background: #0067b2;
  }
}
</style>
