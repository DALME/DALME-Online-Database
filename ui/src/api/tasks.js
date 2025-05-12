import S from "string";

import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tasks`;

const tasks = {
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
  getByUser(userId, limit, offset) {
    return {
      url: `${endpoint}/?user=${userId}&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getCreated(userId, limit, offset) {
    return {
      url: `${endpoint}/?creation_user=${userId}&completed=false&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getAssigned(userId, limit, offset) {
    return {
      url: `${endpoint}/?assignees=${userId}&completed=false&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getCompleted(userId, limit, offset) {
    return {
      url: `${endpoint}/?completed=true&completed_by=${userId}&limit=${limit}&offset=${offset}`,
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
  update(id, data) {
    return {
      url: `${endpoint}/${id}`,
      method: "PUT",
      data: data,
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
  setState(id, action) {
    return {
      url: `${endpoint}/${id}/set_state/`,
      method: "PATCH",
      data: { action: S(action).underscore().s },
    };
  },
};

export default tasks;
