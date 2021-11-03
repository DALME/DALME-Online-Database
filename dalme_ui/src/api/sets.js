import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sets`;

const sets = {
  getSet(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getSets(setType, query) {
    const url = `${endpoint}/?set_type=${setType}&${query}`;
    return new Request(url);
  },
  getSetMembers(id, query) {
    const url = `${endpoint}/${id}/members/?${query}`;
    return new Request(url);
  },
};

export default sets;
