import { apiUrl } from "./config";

const endpoint = `${apiUrl}/groups`;

const groups = {
  list() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getByDataset() {
    return {
      url: `${endpoint}/?properties__type=3&format=select`,
      method: "GET",
    };
  },
};

export default groups;
