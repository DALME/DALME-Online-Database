import { defineStore } from "pinia";
import { isEmpty, mergeDeepLeft } from "ramda";
import { notNully } from "@/utils";
import { useNavStore } from "@/stores/navigation";

class ViewState {
  constructor(state) {
    this.state = state;
    this.timestamp = Date.now();
  }

  get isStale() {
    return Date.now() - this.timestamp > 86400000;
  }
}

export const useViewStore = defineStore("views", {
  state: () => {
    return {
      view: {},
      stored: {},
    };
  },
  getters: {
    /** @returns {boolean} */
    showEditFolioBtn(state) {
      return (
        "tab" in state.view &&
        state.view.tab === "folios" &&
        "folios" in state.view &&
        state.view.folios.length > 0
      );
    },

    /** @returns {number} */
    folioCount(state) {
      return "folios" in state.view ? state.view.folios.length : false;
    },

    /** @returns {object} */
    currentFolioData(state) {
      if (notNully(state.view.folios) && notNully(state.view.currentFolioRef)) {
        return state.view.folios[state.view.currentFolioRef];
      } else {
        return {};
      }
    },

    /** @returns {boolean} */
    currentFolioEditOn() {
      return this.showEditFolioBtn && this.currentFolioData.editOn;
    },
  },
  actions: {
    saveViewState(path) {
      this.stored[path] = new ViewState(this.view);
    },

    deleteViewState(path) {
      delete this.stored[path];
    },

    retrieveViewState(path) {
      console.log("retrieving view state");
      if (path in this.stored) {
        const viewState = this.stored[path];
        if (!viewState.isStale) {
          return viewState;
        } else {
          delete this.deleteViewState(path);
        }
      }
      return null;
    },

    setViewState(target) {
      const nav = useNavStore();
      if (!nav.isSameRoute) {
        this.view = {};
        if (!(isEmpty(target.meta) || target.meta.resetStateOnLoad)) {
          const viewState = this.retrieveViewState(target.fullPath);
          if ("viewDefaults" in target.meta)
            this.view = target.meta.viewDefaults;
          if (viewState) this.mergeValues(viewState.state);
        }
      }
    },

    mergeValues(values) {
      let partial = mergeDeepLeft(this.$state, { view: values });
      this.$patch(partial);
    },
  },
  persist: true,
});
