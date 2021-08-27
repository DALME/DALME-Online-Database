import { apiUrl } from "./config";

const endpoint = `${apiUrl}/languages`;

const languages = {
  getLanguages() {
    return new Request(endpoint);
  },
};

export default languages;
