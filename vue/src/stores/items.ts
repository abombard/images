import { defineStore } from "pinia";

export const useItemStore = defineStore("items", {
  state: () => ({
    items: [],
    strings: [],
    errors: [],
  }),
});
