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
    const showEditPageBtn = computed(() => {
      return (
        "tab" in view.value &&
        view.value.tab === "pages" &&
        "pages" in view.value &&
        view.value.pages.length > 0
      );
    });

    const pageCount = computed(() => ("pages" in view.value ? view.value.pages.length : false));

    const currentPageData = computed(() => {
      if (notNully(view.value.pages) && notNully(view.value.currentPageRef)) {
        return view.value.pages[view.value.currentPageRef];
      } else {
        return {};
      }
    });

    const currentPageEditOn = computed(() => showEditPageBtn.value && currentPageData.value.editOn);

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
      showEditPageBtn,
      pageCount,
      currentPageData,
      currentPageEditOn,
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
