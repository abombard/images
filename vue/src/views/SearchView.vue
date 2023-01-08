<template>
  <ul class="image-gallery" v-if="store.items.length">
    <li v-for="item in store.items" :key="item">
      <img :src="item.path" />
      <p>{{ item.path }}</p>
    </li>
  </ul>
</template>

<style scoped>
.image-gallery {
  margin-top: 2rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.image-gallery>li {
  flex-basis: 600px;
}

.image-gallery>li>img {
  object-fit: cover;
  max-width: 100%;
  height: auto;
  vertical-align: middle;
  border-radius: 5px;
}

.error {
  background-color: tomato;
}
</style>

<script setup lang="ts">
import { useItemStore } from "@/stores/items";

const store = useItemStore();

</script>
