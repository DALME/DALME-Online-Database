import { CSRFUrl, authUrl } from "./config";

const auth = {
  authorize(params) {
    return {
      url: `${authUrl}/authorize/?${params.toString()}`,
      method: "GET",
    };
  },
  authUser() {
    return {
      url: `${authUrl}/userinfo/`,
      method: "GET",
    };
  },
  CSRF() {
    return {
      url: CSRFUrl,
      method: "GET",
    };
  },
  login({ username, password }) {
    return {
      url: `${authUrl}/login/`,
      method: "POST",
      data: { username, password },
    };
  },
  logout(params) {
    return {
      url: `${authUrl}/logout/?${params.toString()}`,
      method: "GET",
    };
  },
  oAuthLogout() {
    return {
      url: `${authUrl}/logout/`,
      method: "GET",
    };
  },
  token(params) {
    const headers = new Headers();
    headers.append("cache-control", "no-cache");
    return {
      url: `${authUrl}/token/`,
      method: "POST",
      headers,
      data: params,
    };
  },
};

export default auth;
