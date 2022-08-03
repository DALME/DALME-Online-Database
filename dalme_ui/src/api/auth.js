import { apiUrl, coreUrl, modalLoginUrl, headers } from "./config";

const auth = {
  login({ username, password }) {
    const url = modalLoginUrl;
    return new Request(url, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ username, password }),
    });
  },
  logout() {
    const url = `${coreUrl}/logout/`;
    return new Request(url, { method: "POST", headers: headers() });
  },
  session() {
    const url = `${apiUrl}/session/retrieve/`;
    return new Request(url);
  },
};

export default auth;
