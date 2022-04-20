import { apiUrl } from "./config";

const endpoint = `${apiUrl}/groups`;

const groups = {
  getGroups() {
    return new Request(endpoint);
  },
  getDatasetGroups() {
    const url = `${endpoint}/?properties__type=3&format=select`;
    return new Request(url);
  },
};

export default groups;
