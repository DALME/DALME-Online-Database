import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sets`;

const sets = {
  getSet(objId) {
    const url = `${endpoint}/${objId}`;
    return new Request(url);
  },
  getSets(setType, query) {
    const url = `${endpoint}/?set_type=${setType}&${query}`;
    return new Request(url);
  },
  getSetMembers(objId, query) {
    const url = `${endpoint}/${objId}/members/?${query}`;
    return new Request(url);
  },
};

export default sets;
