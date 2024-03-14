import { apiUrl } from "./config";

const endpoint = `${apiUrl}/groups`;

const groups = {
  getGroups() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
  getDatasetGroups() {
    return {
      url: `${endpoint}/?properties__type=3&format=select`,
      method: "GET",
    };
  },
};

export default groups;
