import { apiUrl } from "./config";

const endpoint = `${apiUrl}/languages`;

const languages = {
  list(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
  getCompletions(language, data) {
    const url = `${endpoint}/${language}/completions/`;
    return {
      url: url,
      method: "POST",
      data: data,
    };
  },
};

export default languages;
