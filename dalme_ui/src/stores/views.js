import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { isEmpty, mergeDeepLeft } from "ramda";
import { notNully } from "@/utils";
import { useUiStore } from "@/stores/ui";

class ViewState {
  constructor(state) {
    this.state = state;
    this.timestamp = Date.now();
  }

  get isStale() {
    return Date.now() - this.timestamp > 86400000;
  }
}

export const useViewStore = defineStore(
  "views",
  () => {
    // stores
    const ui = useUiStore();

    // state
    const view = ref({});
    const stored = ref({});

    // getters
    const showEditFolioBtn = computed(() => {
      return (
        "tab" in view.value &&
        view.value.tab === "folios" &&
        "folios" in view.value &&
        view.value.folios.length > 0
      );
    });

    const folioCount = computed(() => ("folios" in view.value ? view.value.folios.length : false));

    const currentFolioData = computed(() => {
      if (notNully(view.value.folios) && notNully(view.value.currentFolioRef)) {
        return view.value.folios[view.value.currentFolioRef];
      } else {
        return {};
      }
    });

    const currentFolioEditOn = computed(
      () => showEditFolioBtn.value && currentFolioData.value.editOn,
    );

    // actions
    const $reset = () => {
      view.value = {};
      stored.value = {};
    };

    const saveViewState = (path) => {
      stored.value[path] = new ViewState(view.value);
    };

    const deleteViewState = (path) => {
      delete stored.value[path];
    };

    const retrieveViewState = (path) => {
      if (path in stored.value) {
        const viewState = stored.value[path];
        if (!viewState.isStale) {
          return viewState;
        } else {
          deleteViewState(path);
        }
      }
      return null;
    };

    const setViewState = (store, target) => {
      if (!ui.isSameRoute) {
        view.value = {};
        if (!(isEmpty(target.meta) || target.meta.resetStateOnLoad)) {
          const viewState = retrieveViewState(target.fullPath);
          if ("viewDefaults" in target.meta) view.value = target.meta.viewDefaults;
          if (viewState) mergeValues(store, viewState.state);
        }
      }
    };

    const mergeValues = (store, values) => {
      let partial = mergeDeepLeft(store.$state, { view: values });
      store.$patch(partial);
    };

    return {
      mergeValues,
      view,
      stored,
      showEditFolioBtn,
      folioCount,
      currentFolioData,
      currentFolioEditOn,
      saveViewState,
      deleteViewState,
      retrieveViewState,
      setViewState,
      $reset,
    };
  },
  {
    persist: true,
  },
);
