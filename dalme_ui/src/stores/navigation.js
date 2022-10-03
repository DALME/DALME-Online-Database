import { defineStore } from "pinia";

export const useNavStore = defineStore("navigation", {
  state: () => {
    return {
      currentSection: "",
      currentSubsection: "",
      breadcrumbTail: [],
      currentPageIcon: "",
    };
  },
  getters: {
    breadcrumb: (state) => {
      return [state.currentSection, state.currentSubsection].concat(
        state.breadcrumbTail,
      );
    },
  },
  actions: {
    resetBreadcrumbTail() {
      this.breadcrumbTail = [];
    },
  },
  persist: {
    afterRestore: (ctx) => {
      ctx.store.resetBreadcrumbTail();
    },
  },
});
