import { apiUrl } from "./config";
import { worksetId } from "./constants";

const endpoint = `${apiUrl}/sets`;
const v2Endpoint = `${apiUrl}/v2/sets`;

const sets = {
  createSet(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  editSet(id, data) {
    return {
      url: `${endpoint}/${id}/`,
      method: "PUT",
      data: data,
    };
  },
  getSet(id) {
    return {
      url: `${endpoint}/${id}`,
      method: "GET",
    };
  },
  getSets() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
  getSetsByType(setType, query) {
    let url = `${endpoint}/?set_type=${setType}`;
    if (query) {
      url = `${url}&${query}`;
    }
    return {
      url: url,
      method: "GET",
    };
  },
  getSetMembers(id, query) {
    return {
      url: `${endpoint}/${id}/members/?${query}`,
      method: "GET",
    };
  },
  getUserWorksets(userId) {
    return {
      url: `${v2Endpoint}/?type=${worksetId}&owner=${userId}`,
      method: "GET",
    };
  },
};

export default sets;
