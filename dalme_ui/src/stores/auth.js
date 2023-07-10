import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { API as apiInterface, publicUrl, requests } from "@/api";
import { notNully } from "@/utils";
import notifier from "@/notifier";
import { useUiStore } from "@/stores/ui";
import { useViewStore } from "@/stores/views";

export const useAuthStore = defineStore(
  "auth",
  () => {
    // stores
    const ui = useUiStore();
    const views = useViewStore();

    // state
    const userId = ref(null);
    const username = ref("");
    const fullName = ref("");
    const email = ref("");
    const avatar = ref("");
    const isAdmin = ref(false);
    const preferences = ref({
      general: {
        tooltipsOn: true,
        sidebarCollapsed: false,
      },
      sourceEditor: {},
      lists: {},
    });
    const groups = ref([]);
    const reAuthenticate = ref(false);
    const isRefreshing = ref(false);
    const requestQueue = ref([]);

    // getters
    const hasCredentials = computed(() => notNully(userId.value));

    // actions
    const $reset = () => {
      userId.value = null;
      username.value = "";
      fullName.value = "";
      email.value = "";
      avatar.value = "";
      isAdmin.value = false;
      preferences.value = {
        general: {
          tooltipsOn: true,
          sidebarCollapsed: false,
        },
        sourceEditor: {},
        lists: {},
      };
      groups.value = [];
      reAuthenticate.value = false;
      isRefreshing.value = false;
      requestQueue.value = [];
    };

    const login = async (data) => {
      userId.value = data.id;
      username.value = data.username;
      fullName.value = data.fullName;
      email.value = data.email;
      avatar.value = data.avatar;
      isAdmin.value = data.isAdmin;
      reAuthenticate.value = false;
      isRefreshing.value = false;
      groups.value = data.groups;
      if (notNully(data.preferences)) {
        preferences.value = data.preferences;
      }
    };

    const logout = async () => {
      ui.$reset();
      views.$reset();
      $reset();
      const { fetchAPI, success, redirected } = apiInterface();
      await fetchAPI(requests.auth.logout());
      if (success.value) {
        if (redirected) {
          window.location.href = publicUrl;
        }
      }
    };

    const processQueue = async () => {
      await requestQueue.value.forEach((callback) => callback());
      requestQueue.value = [];
    };

    const updatePreferences = async (id, route, mutation) => {
      const { newValue, key, target } = mutation.events;
      const useKey = Array.isArray(target) ? route : key;
      const section = getSectionfromKey(useKey);
      const useValue = Array.isArray(target) ? preferences.value[section][useKey] : newValue;
      const { fetchAPI, success } = apiInterface();
      if (notNully(section)) {
        await fetchAPI(requests.users.updateUserPreferences(id, section, useKey, useValue));
        if (!success.value) {
          notifier.users.prefUpdateFailed();
        }
      }
    };

    const getSectionfromKey = (key) => {
      for (const section of Object.keys(preferences.value)) {
        if (Object.keys(preferences.value[section]).indexOf(key) > -1) {
          return section;
        }
      }
      return null;
    };

    return {
      userId,
      username,
      fullName,
      email,
      avatar,
      isAdmin,
      preferences,
      groups,
      reAuthenticate,
      isRefreshing,
      requestQueue,
      hasCredentials,
      login,
      logout,
      processQueue,
      updatePreferences,
      $reset,
    };
  },
  {
    persist: true,
  },
);
