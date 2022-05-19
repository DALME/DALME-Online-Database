import { apiUrl, headers } from "./config";
import { worksetId } from "./constants";

const endpoint = `${apiUrl}/sets`;
const v2Endpoint = `${apiUrl}/v2/sets`;

const sets = {
  createSet(data) {
    const url = `${endpoint}/`;
    return new Request(url, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify(data),
    });
  },
  editSet(id, data) {
    const url = `${endpoint}/${id}/`;
    return new Request(url, {
      method: "PUT",
      headers: headers(),
      body: JSON.stringify(data),
    });
  },
  getSet(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getSets() {
    return new Request(endpoint);
  },
  getSetsByType(setType, query) {
    let url = `${endpoint}/?set_type=${setType}`;
    if (query) {
      url = `${url}&${query}`;
    }
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
