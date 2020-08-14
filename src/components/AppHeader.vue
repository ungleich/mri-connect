<template>
  <div class="header">
    <vs-navbar
        color="secondary"
        text-color="rgba(255,255,255,1)"
        class="navbar"
    >

      <div slot="title">
        <vs-navbar-title>
          <router-link to="/">
            <img class="logo" src="@/assets/MRI_logo_black.svg" alt="logo">
          </router-link>
        </vs-navbar-title>
      </div>
      <vs-navbar-item>
        <a href="mailto:info@datalets.ch" target="_blank">Contact</a>
      </vs-navbar-item>
      <vs-navbar-item>
        <a href="https://github.com/datalets/mri-connect" target="_blank">Source</a>
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
  margin-bottom: 2em;
}
.vs-navbar--title {
  img {
    height: 80px;
  }
  a {
    color: black;
    u {
      border-bottom: 2px solid blue;
    }
  }
}
</style>
