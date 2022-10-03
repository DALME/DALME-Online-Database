import { apiUrl } from "./config";

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
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getSets(query = false) {
    const url = query
      ? `${endpoint}/?${query}`
      : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
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
      url: `${v2Endpoint}/?type=4&owner=${userId}`,
      method: "GET",
    };
  },
};

export default sets;
