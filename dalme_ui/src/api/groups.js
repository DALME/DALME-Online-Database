import { apiUrl } from "./config";

const endpoint = `${apiUrl}/groups`;

const groups = {
  getGroups() {
    return new Request(endpoint);
  },
};

export default groups;
