<template>
  <div class="search">
    <input @keyup.enter=search() type="text" v-model="input" placeholder="Search .." />
    <div class="item" v-for="image in store.items" :key="image">
      <p>{{ image }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { useItemStore } from "@/stores/items"

let input = ref("");

const hostname = "http://localhost:5174"
const store = useItemStore();

function search() {
  axios
    .post(`{hostname}/search`, { text: input.value })
    .then(response => {
      console.log(response.data);
      store.$patch({ items: response.data.response.items });
    })
    .catch(error => {
      store.$patch({ items: ["No results found", error] });
    })
}
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Montserrat&display=swap");

@media (min-width: 1024px) {
  .search {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: left;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-family: "Montserrat", sans-serif;
  }

  input {
    display: block;
    width: 350px;
    margin: 20px auto;
    padding: 10px 45px;
    background: white url("assets/search-icon.svg") no-repeat 15px center;
    background-size: 15px 15px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
      rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  }

  .item {
    width: 350px;
    margin: 0 auto 10px auto;
    padding: 10px 20px;
    color: white;
    border-radius: 5px;
    background-color: hsla(160, 100%, 37%, 1);
    box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 3px 0px,
      rgba(0, 0, 0, 0.06) 0px 1px 2px 0px;
  }

  .image {
    background-color: rgb(97, 62, 252);
    cursor: pointer;
  }

  .error {
    background-color: tomato;
  }
}
</style>
