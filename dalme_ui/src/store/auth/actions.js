import { API as apiInterface, loginUrl, requests } from "@/api";

export const login = ({ commit }, data) => commit("addUser", data);

export const logout = async ({ commit }) => {
  commit("deleteUser");
  const { fetchAPI, redirected } = apiInterface();
  await fetchAPI(requests.auth.logout());
  if (redirected) {
    window.location.href = `${loginUrl}?next=/ui/`;
  }
};
