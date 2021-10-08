import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/locales`;

const locales = {
  getLocales() {
    return new Request(endpoint);
  },
  updateLocales(data) {
    const url = `${endpoint}/update_locales/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify(data.value),
    });
  },
};

export default locales;
