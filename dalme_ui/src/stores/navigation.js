import { defineStore } from "pinia";

export const useNavStore = defineStore("navigation", {
  state: () => {
    return {
      previousPath: "",
      currentPath: "",
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
    isSameRoute: (state) => {
      return state.previousPath === state.currentPath;
    },
  },
  actions: {
    resetBreadcrumbTail() {
      this.breadcrumbTail = [];
    },

    async setPageState(target) {
      this.previousPath = this.currentPath;
      this.currentPath = target.fullPath;
      this.currentSection = target.meta.navPath[0];
      this.currentSubsection = target.meta.navPath[1];
      this.currentPageIcon = target.meta.icon || "layers";
      this.resetBreadcrumbTail();
    },
  },
  persist: {
    afterRestore: (ctx) => {
      ctx.store.resetBreadcrumbTail();
    },
  },
});
