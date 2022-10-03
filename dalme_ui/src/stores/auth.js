import { defineStore } from "pinia";
import { API as apiInterface, publicUrl, requests } from "@/api";
import { usePrefStore } from "@/stores/preferences";
import { useNotifier } from "@/use";
import { isNil } from "ramda";

export const useAuthStore = defineStore("auth", {
  state: () => {
    return {
      userId: null,
      username: "",
      fullName: "",
      email: "",
      avatar: "",
      isAdmin: null,
      reAuthenticate: false,
      isRefreshing: false,
      requestQueue: [],
    };
  },
  getters: {
    hasCredentials: (state) => !isNil(state.userId),
  },
  actions: {
    async login(data) {
      this.userId = data.id;
      this.username = data.username;
      this.fullName = data.fullName;
      this.email = data.email;
      this.avatar = data.avatar;
      this.isAdmin = data.isAdmin;
    },
    async logout() {
      const prefStore = usePrefStore();
      prefStore.$reset();
      this.$reset();
      const { fetchAPI, success, redirected } = apiInterface();
      await fetchAPI(requests.auth.logout());
      if (success.value) {
        if (redirected) {
          window.location.href = publicUrl;
        }
      } else {
        const $notifier = useNotifier();
        $notifier.auth.logoutFailed();
      }
    },
    async processQueue() {
      await this.requestQueue.forEach((callback) => callback());
      this.requestQueue = [];
    },
  },
  persist: true,
});
