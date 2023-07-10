import S from "string";
import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tasks`;

const tasks = {
  getTasks(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  getTask(id) {
    return {
      url: `${endpoint}/${id}`,
      method: "GET",
    };
  },
  getUserTasks(userId, limit) {
    return {
      url: `${endpoint}/?user=${userId}&limit=${limit}`,
      method: "GET",
    };
  },
  getCreatedTasks(userId, limit, offset = 0) {
    return {
      url: `${endpoint}/?creation_user=${userId}&completed=false&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getAssignedTasks(userId, limit) {
    return {
      url: `${endpoint}/?assignees=${userId}&completed=false&limit=${limit}`,
      method: "GET",
    };
  },
  getCompletedTasks(userId, limit) {
    return {
      url: `${endpoint}/?completed=true&completed_by=${userId}&limit=${limit}`,
      method: "GET",
    };
  },
  createTask(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  editTask(id, data) {
    return {
      url: `${endpoint}/${id}`,
      method: "PUT",
      data: data,
    };
  },
  setTaskState(id, action) {
    return {
      url: `${endpoint}/${id}/set_state/`,
      method: "PATCH",
      data: { action: S(action).underscore().s },
    };
  },
  getUserTasklists(userId) {
    return {
      url: `${apiUrl}/tasklists/?user=${userId}`,
      method: "GET",
    };
  },
  getTasklists() {
    return {
      url: `${apiUrl}/tasklists/`,
      method: "GET",
    };
  },
  getTasklist(id) {
    return {
      url: `${apiUrl}/tasklists/${id}`,
      method: "GET",
    };
  },
  createTasklist(data) {
    return {
      url: `${apiUrl}/tasklists/`,
      method: "POST",
      data: data,
    };
  },
  deleteTasklist(id) {
    return {
      url: `${apiUrl}/tasklists/${id}`,
      method: "DELETE",
    };
  },
  editTasklist(id, data) {
    return {
      url: `${apiUrl}/tasklists/${id}/`,
      method: "PUT",
      data: data,
    };
  },
};

export default tasks;
