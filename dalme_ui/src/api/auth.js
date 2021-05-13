import {
  apiUrl,
  dbUrl,
  loginUrl,
  modalLoginUrl,
  fetchApi,
  headers,
} from "./config";

const auth = {
  async login(form) {
    const url = modalLoginUrl;
    const request = new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(form),
    });

    const response = await fetchApi(request);
    const data = await response.json();

    return { success: response.ok, data };
  },

  async logout() {
    const url = `${dbUrl}/logout/`;
    const request = new Request(url, { method: "POST", headers: headers });

    const response = await fetchApi(request);

    if (response.redirected) {
      window.location.href = `${loginUrl}?next=/ui/`;
    }
  },

  async session() {
    const url = `${apiUrl}/session/retrieve/`;
    const request = new Request(url);

    const response = await fetchApi(request);
    const data = await response.json();

    return { success: response.ok, data };
  },
};

export default auth;
