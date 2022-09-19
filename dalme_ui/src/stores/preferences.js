import { defineStore } from "pinia";
import { API as apiInterface, requests } from "@/api";
import { useNotifier } from "@/use";
import { isEmpty, isNil } from "ramda";

export const usePrefStore = defineStore("preferences", {
  state: () => {
    return {
      ui: {
        tooltipsOn: true,
        sidebarCollapsed: false,
      },
      sourceEditor: {},
      lists: {},
    };
  },
  actions: {
    async loadPreferences(prefs) {
      if (!isEmpty(prefs) && !isNil(prefs)) {
        this.$patch(prefs);
      }
    },
    async updatePreferences(userId, route, mutation) {
      const { newValue, key, target } = mutation.events;
      let useKey = Array.isArray(target) ? route : key;
      let useValue = Array.isArray(target) ? target : newValue;
      const section = this.getSectionfromKey(useKey);
      const $notifier = useNotifier();
      const { fetchAPI, success } = apiInterface();
      if (!isEmpty(section) && !isNil(section)) {
        await fetchAPI(
          requests.users.updateUserPreferences(
            userId,
            section,
            useKey,
            useValue,
          ),
        );
        if (!success.value) {
          $notifier.users.prefUpdateFailed();
        }
      }
    },
    getSectionfromKey(key) {
      for (const section of Object.keys(this.$state)) {
        if (Object.keys(this[section]).indexOf(key) > -1) {
          return section;
        }
      }
      return null;
    },
  },
  persist: {
    // https://prazdevs.github.io/pinia-plugin-persistedstate/guide/config.html
    storage: sessionStorage, // default is localStorage
  },
});
