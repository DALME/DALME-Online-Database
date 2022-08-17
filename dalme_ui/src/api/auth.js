import { loginUrl, logoutUrl, tokenRefreshUrl } from "./config";

const auth = {
  login({ username, password }) {
    return {
      url: loginUrl,
      method: "POST",
      data: { username, password },
    };
  },
  logout() {
    return {
      url: logoutUrl,
      method: "POST",
    };
  },
  refreshToken() {
    return {
      url: tokenRefreshUrl,
      method: "POST",
    };
  },
};

export default auth;
