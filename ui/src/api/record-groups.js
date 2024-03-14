import { apiUrl } from "./config";

const endpoint = `${apiUrl}/record-groups`;

const recordGroups = {
  getRecordGroup(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getRecordGroups(query) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/`;
    return {
      url: url,
      method: "GET",
    };
  },
};

export default recordGroups;
