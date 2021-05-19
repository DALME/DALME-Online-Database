import { apiUrl, dbUrl, modalLoginUrl, headers } from "./config";

const auth = {
  login(form) {
    const url = modalLoginUrl;
    return new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(form),
    });
  },

  logout() {
    const url = `${dbUrl}/logout/`;
    return new Request(url, { method: "POST", headers: headers });
  },

  session() {
    const url = `${apiUrl}/session/retrieve/`;
    return new Request(url);
  },
};

export default auth;
