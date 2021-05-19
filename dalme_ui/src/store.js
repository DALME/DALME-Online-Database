import { createStore } from "vuex";

import { API as useAPI, loginUrl, requests } from "@/api";

const store = createStore({
  state: {
    user: null,
  },
  getters: {
    isAuthenticated(state) {
      return state.user !== null;
    },
    userId(state) {
      return state.user.id;
    },
  },
  mutations: {
    addUser(state, data) {
      state.user = data;
    },
    deleteUser(state) {
      state.user = null;
    },
  },
  actions: {
    login({ commit }, data) {
      commit("addUser", data);
    },
    async logout({ commit }) {
      commit("deleteUser");
      const { fetchAPI, redirected } = useAPI();
      await fetchAPI(requests.auth.logout());
      if (redirected) {
        window.location.href = `${loginUrl}?next=/ui/`;
      }
    },
  },
});

export default store;
