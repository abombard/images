<template>
  <div>
    <input id="file-input" class="hide-file-input" type="file" accept="image/*" @change="onFileChange($event)" />
    <label class="file-btn" for="file-input">Search from image</label>
  </div>
</template>

<script setup lang="ts">
import { search } from "@/search";

const onFileChange = (event) => {
  const file = event.target.files[0];

  search({ image: file.name });
}
</script>

<style scoped>
.hide-file-input {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.file-btn {
  height: 3rem;
  width: 12rem;
  background: var(--color-header-button);
  color: var(--color-header-text);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
}

.file-btn:hover {
  background: var(--color-header-button-hover);
}
</style>
