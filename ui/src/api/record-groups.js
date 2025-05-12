import { apiUrl } from "./config";

const endpoint = `${apiUrl}/record-groups`;

const recordGroups = {
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  list(query) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/`;
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
};

export default recordGroups;
