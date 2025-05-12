import { apiUrl } from "./config";

const endpoint = `${apiUrl}/collections`;

const collections = {
  create(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  update(id, data) {
    return {
      url: `${endpoint}/${id}/`,
      method: "PUT",
      data: data,
    };
  },
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  list(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
  getMembers(id, query) {
    return {
      url: `${endpoint}/${id}/members/?${query}`,
      method: "GET",
    };
  },
  getByUser(userId, limit) {
    return {
      url: `${endpoint}/?owner=${userId}&limit=${limit}`,
      method: "GET",
    };
  },
  getByTeam(userId, limit) {
    return {
      url: `${endpoint}/?owner=${userId}&limit=${limit}`,
      method: "GET",
    };
  },
};

export default collections;
