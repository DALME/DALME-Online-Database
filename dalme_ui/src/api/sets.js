import { apiUrl } from "./config";
import { worksetId } from "./constants";

const endpoint = `${apiUrl}/sets`;
const v2Endpoint = `${apiUrl}/v2/sets`;

const sets = {
  getSet(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getSets() {
    return new Request(endpoint);
  },
  getSetsByType(setType, query) {
    const url = `${endpoint}/?set_type=${setType}&${query}`;
    return new Request(url);
  },
  getSetMembers(id, query) {
    const url = `${endpoint}/${id}/members/?${query}`;
    return new Request(url);
  },
  getUserWorksets(userId) {
    const url = `${v2Endpoint}/?type=${worksetId}&owner=${userId}`;
    return new Request(url);
  },
};

export default sets;
