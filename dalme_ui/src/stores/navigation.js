import { defineStore } from "pinia";

export const useNavStore = defineStore("navigation", {
  state: () => {
    return {
      currentSection: "",
      currentSubsection: "",
    };
  },
  getters: {},
  actions: {},
});
