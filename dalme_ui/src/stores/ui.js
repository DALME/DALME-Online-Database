import { defineStore } from "pinia";
import { useViewStore } from "@/stores/views";
import { useNavStore } from "@/stores/navigation";

export const useUiStore = defineStore("ui", {
  state: () => {
    return {
      globalLoading: false,
      compactMode: false,
      allowCompactMode: false,
      isFullscreen: false,
      windowHeight: window.innerHeight,
      windowWidth: window.innerWidth,
      stripExpanded: false,
      stripKeepOpen: false,
      drawerExpanded: false,
      folioIndexShow: false,
      inlineIndexShow: false,
      windowIndexShow: false,
      currentFolioEdit: false,
      stripApproachHover: false,
    };
  },
  getters: {
    /** @returns {number} */
    containerHeight(state) {
      const headerHeight = state.compactMode ? 153 : 279;
      const chrome = headerHeight + 32;
      return this.windowHeight - chrome;
    },

    /** @returns {number} */
    containerWidth(state) {
      const views = useViewStore();
      let chrome = 84;
      if ("folioDrawerMini" in views.view && views.view.folioDrawerMini.value)
        chrome = chrome + 149;
      return this.windowWidth - chrome;
    },
  },
  actions: {
    onWindowResize() {
      this.windowHeight = window.innerHeight;
      this.windowWidth = window.innerWidth;
    },

    resizeListener() {
      window.addEventListener("resize", this.onWindowResize);
    },

    setUiState(target) {
      const nav = useNavStore();
      this.allowCompactMode = target.meta.allowCompactMode || false;
      this.compactMode = nav.isSameRoute ? this.compactMode : false;
      this.stripExpanded = this.stripKeepOpen ? true : false;
      this.drawerExpanded = nav.isSameRoute ? this.drawerExpanded : false;
      this.currentFolioEdit = nav.isSameRoute ? this.currentFolioEdit : false;
    },
  },
  persist: true,
});
