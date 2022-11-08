import { defineStore } from "pinia";
import { isEmpty, mergeDeepLeft } from "ramda";

export const useUiStore = defineStore("uiStore", {
  state: () => {
    return {
      globalLoading: false,
      compactMode: false,
      compactModeDisable: true,
      isFullscreen: false,
      windowHeight: window.innerHeight,
      windowWidth: window.innerWidth,
      view: {
        viewLoading: false,
      },
      editPanel: {
        stripExpanded: false,
        stripKeepOpen: false,
        drawerExpanded: false,
        folioIndexShow: false,
        inlineIndexShow: false,
        windowIndexShow: false,
        currentFolioEdit: false,
        stripApproachHover: false,
      },
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
      const folioDrawerWidth = state.view.folioDrawerMini ? 0 : 149;
      const chrome = folioDrawerWidth + 42 + 42;
      return this.windowWidth - chrome;
    },

    /** @returns {boolean} */
    showEditFolioBtn(state) {
      return (
        "tab" in state.view &&
        state.view.tab === "folios" &&
        "folios" in state.view &&
        state.view.folios.length > 0
      );
    },

    /** @returns {boolean} */
    currentFolioEditOn(state) {
      return (
        this.showEditFolioBtn &&
        state.view.folios[state.view.currentFolio].editOn
      );
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

    resetViewState(meta) {
      if (!isEmpty(meta)) {
        const allowCompactMode = meta.allowCompactMode || false;
        const preserveCompactMode = meta.preserveCompactMode || false;
        const usesPersistedUi = meta.usesPersistedUi || false;

        if (!allowCompactMode) {
          this.compactModeDisable = true;
          this.compactMode = false;
        } else {
          this.compactModeDisable = false;
          if (!preserveCompactMode) {
            this.compactMode = false;
          }
        }
        if (!usesPersistedUi) {
          console.log("resetting viewPersistence");
          this.view = {};
        }
      } else {
        console.log("full reset!");
        this.reset();
      }
      this.editPanel.folioIndexShow = false;
      this.editPanel.currentFolioEdit = false;
    },

    mergeValues(values) {
      let partial = mergeDeepLeft(this.$state, values);
      this.$patch(partial);
    },
  },
  persist: true,
});
