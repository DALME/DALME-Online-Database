import { API as useAPI, loginUrl, requests } from "@/api";

export const login = ({ commit }, data) => commit("addUser", data);

export const logout = async ({ commit }) => {
  commit("deleteUser");
  const { fetchAPI, redirected } = useAPI();
  await fetchAPI(requests.auth.logout());
  if (redirected) {
    window.location.href = `${loginUrl}?next=/ui/`;
  }
};
