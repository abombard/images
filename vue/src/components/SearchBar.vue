<template>
  <input @keyup.enter="searchtext()" type="text" v-model="input" placeholder="Search from text" />
</template>

<style scoped>
input[type="text"] {
  height: 2.5rem;
  width: 12rem;
  padding: 0.5rem 1rem;
  border: none;
  box-shadow: var(--color-black), var(--color-back);
}
</style>

<script setup lang="ts">
import { ref } from "vue";
import { search } from "@/search.ts";

let input = ref("");

const searchtext = () => {
  search({ text: input.value });
}
</script>

