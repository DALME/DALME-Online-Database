import { apiUrl } from "./config";

const endpoint = `${apiUrl}/locations`;

const locations = {
  list(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
};

export default locations;
