import { defineStore } from "pinia";
import { isEmpty, mergeDeepLeft } from "ramda";
import { computed, ref } from "vue";

import { useUiStore } from "@/stores/ui";
import { nully } from "@/utils";

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
    const showEditBtn = computed(() => {
      return (
        "tab" in view.value &&
        view.value.tab === "pages" &&
        "pages" in view.value &&
        view.value.pages.length > 0
      );
    });

    const pageCount = computed(() => ("pages" in view.value ? view.value.pages.length : false));

    const currentPageData = computed(() => {
      if (!nully(view.value.pages) && !nully(view.value.currentPageRef)) {
        return view.value.pages[view.value.currentPageRef];
      } else {
        return {};
      }
    });

    const editOn = computed(() => showEditBtn.value && view.value.editOn);

    const hasChanges = computed(
      () => "pages" in view.value && view.value.pages.some((p) => p.dbTei !== p.tei),
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
      showEditBtn,
      pageCount,
      currentPageData,
      editOn,
      saveViewState,
      deleteViewState,
      retrieveViewState,
      setViewState,
      hasChanges,
      $reset,
    };
  },
  {
    persist: true,
  },
);
