<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import SearchBar from "./components/SearchBar.vue"
import DownloadFile from "./components/DownloadFile.vue"
</script>

<template>
  <header>
    <div class="nav-left-elem-list">
      <SearchBar class="nav-left-elem" />
      <DownloadFile class="nav-left-elem" />
    </div>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">About</RouterLink>
      <RouterLink to="/search">Search</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  width: 100vw;
  max-height: 80vh;
  line-height: 1.5;
  z-index: 200;
  background: var(--color-header-background);
  opacity: 0.8;
  font-size: 25px;
  display: flex;
  justify-content: space-between;
  height: 70px;
}

.nav-left-elem-list {
  margin-left: 1rem;
  display: flex;
  align-items: center;
}

.nav-left-elem {
  padding: 1rem;
  border-radius: 5px;
}

nav {
  text-align: right;
}

nav a.router-link-exact-active {
  background: var(--color-header-nav-button-active);
}

nav a {
  display: inline-block;
  padding: 1rem;
  border-left: 1px solid var(--color-header-nav-button-sep);
  color: var(--color-header-text);
}

nav a:hover {
  background: var(--color-header-nav-button-hover);
}

nav a:first-of-type {
  border: 0;
}
</style>
