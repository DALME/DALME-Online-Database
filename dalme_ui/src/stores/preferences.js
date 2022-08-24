import { defineStore } from "pinia";
import { API as apiInterface, requests } from "@/api";
import { useNotifier } from "@/use";
import { useAuthStore } from "@/stores/auth";

export const usePrefStore = defineStore("preferences", {
  state: () => {
    return {
      ui: {
        tooltipsOn: true,
        sidebarCollapsed: false,
      },
      sourceEditor: {
        fontSize: "14",
        highlightWord: true,
        showGuides: true,
        showGutter: true,
        showInvisibles: false,
        showLineNumbers: true,
        softWrap: true,
        theme: "Chrome",
      },
    };
  },
  actions: {
    async loadPreferences(prefs) {
      this.ui.tooltipsOn = prefs.ui.tooltipsOn;
      this.ui.sidebarCollapsed = prefs.ui.sidebarCollapsed;
      this.sourceEditor = prefs.sourceEditor;
    },
    toggleSubscription() {
      const authStore = useAuthStore();
      this.$subscribe(
        (state) => {
          this.updatePreferences(authStore.userId, state);
        },
        { detached: true },
      );
    },
    async updatePreferences(userId, state) {
      const { newValue, key } = state.events;
      const section = this.getSectionfromKey(key);
      const $notifier = useNotifier();
      const { fetchAPI, success } = apiInterface();
      await fetchAPI(
        requests.users.updateUserPreferences(userId, section, key, newValue),
      );
      if (success.value) {
        $notifier.users.prefUpdateSuccess();
      } else {
        $notifier.users.prefUpdateFailed();
      }
    },
    getSectionfromKey(key) {
      let result = null;
      Object.keys(this.$state).forEach((section) => {
        if ({}.propertyIsEnumerable.call(this[section], key)) result = section;
      });
      return result;
    },
  },
  persist: {
    // https://prazdevs.github.io/pinia-plugin-persistedstate/guide/config.html
    storage: sessionStorage, // default is localStorage
  },
});
