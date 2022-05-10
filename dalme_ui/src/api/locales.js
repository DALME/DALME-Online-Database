import { apiUrl } from "./config";

const endpoint = `${apiUrl}/locales`;

const locales = {
  getLocales() {
    return new Request(endpoint);
  },
};

export default locales;
