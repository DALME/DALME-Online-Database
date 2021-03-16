import { apiUrl, dbUrl, fetchApi, headers } from "./config";

const auth = {
  async logout() {
    const url = `${dbUrl}/logout/`;
    const request = new Request(url, { method: "POST", headers: headers });

    const response = await fetchApi(request);
    if (response.redirected) {
      window.location.href = response.url;
    } else {
      const data = await response.json();
      throw data;
    }
  },

  async session() {
    const url = `${apiUrl}/session/retrieve/`;
    const request = new Request(url);

    const response = await fetchApi(request);
    return response;
  },
};

export default auth;
