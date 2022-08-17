import { defineStore } from "pinia";
import { API as apiInterface, publicUrl, requests } from "@/api";
import { isNil } from "ramda";

export const useAuthStore = defineStore("auth", {
  state: () => {
    return {
      id: null,
      username: "",
      full_name: "",
      email: "",
      avatar: "",
      isAdmin: null,
      reAuthenticate: false,
      isRefreshing: false,
      requestQueue: [],
    };
  },
  getters: {
    hasCredentials: (state) => !isNil(state.id),
  },
  actions: {
    async login(data) {
      this.id = data.user.id;
      this.username = data.user.username;
      this.full_name = data.user.full_name;
      this.email = data.user.email;
      this.avatar = data.user.avatar;
      this.isAdmin = data.user.isAdmin;
    },
    async logout() {
      this.$reset();
      const { fetchAPI, status, redirected } = apiInterface();
      await fetchAPI(requests.auth.logout());
      if (status.value === 200) {
        if (redirected) {
          window.location.href = publicUrl;
        }
      } else {
        console.log("raise error");
      }
    },
    async processQueue() {
      await this.requestQueue.forEach((callback) => callback());
      this.requestQueue = [];
    },
  },
  persist: {
    // https://prazdevs.github.io/pinia-plugin-persistedstate/guide/config.html
    storage: sessionStorage, // default is localStorage
  },
});
