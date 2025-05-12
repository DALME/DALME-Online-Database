import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tasklists`;

const taskLists = {
  getByUser(userId, limit, offset) {
    return {
      url: `${endpoint}/?user=${userId}&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  list(query, limit, offset) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=${limit}&offset=${offset}`;
    return {
      url: url,
      method: "GET",
    };
  },
  get(id) {
    return {
      url: `${endpoint}/${id}`,
      method: "GET",
    };
  },
  create(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  destroy(id) {
    return {
      url: `${endpoint}/${id}`,
      method: "DELETE",
    };
  },
  update(id, data) {
    return {
      url: `${endpoint}/${id}/`,
      method: "PUT",
      data: data,
    };
  },
};

export default taskLists;
