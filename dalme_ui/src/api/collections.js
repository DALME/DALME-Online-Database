import { apiUrl } from "./config";

const endpoint = `${apiUrl}/collections`;

const collections = {
  createCollection(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  editCollection(id, data) {
    return {
      url: `${endpoint}/${id}/`,
      method: "PUT",
      data: data,
    };
  },
  getCollection(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getCollections(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  getCollectionMembers(id, query) {
    return {
      url: `${endpoint}/${id}/members/?${query}`,
      method: "GET",
    };
  },
  getUserCollections(userId, limit) {
    return {
      url: `${endpoint}/?owner=${userId}&limit=${limit}`,
      method: "GET",
    };
  },
  getTeamCollections(userId, limit) {
    return {
      url: `${endpoint}/?owner=${userId}&limit=${limit}`,
      method: "GET",
    };
  },
};

export default collections;
