import { apiUrl } from "./config";

const endpoint = `${apiUrl}/locales`;

const locales = {
  getLocales() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
};

export default locales;
