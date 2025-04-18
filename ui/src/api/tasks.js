import S from "string";

import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tasks`;

const tasks = {
  getTasks(query, limit, offset) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=${limit}&offset=${offset}`;
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
  getUserTasks(userId, limit, offset) {
    return {
      url: `${endpoint}/?user=${userId}&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getCreatedTasks(userId, limit, offset) {
    return {
      url: `${endpoint}/?creation_user=${userId}&completed=false&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getAssignedTasks(userId, limit, offset) {
    return {
      url: `${endpoint}/?assignees=${userId}&completed=false&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getCompletedTasks(userId, limit, offset) {
    return {
      url: `${endpoint}/?completed=true&completed_by=${userId}&limit=${limit}&offset=${offset}`,
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
  getUserTaskLists(userId, limit, offset) {
    return {
      url: `${apiUrl}/tasklists/?user=${userId}&limit=${limit}&offset=${offset}`,
      method: "GET",
    };
  },
  getTaskLists(query, limit, offset) {
    const url = query
      ? `${apiUrl}/tasklists/?${query}`
      : `${apiUrl}/tasklists/?limit=${limit}&offset=${offset}`;
    return {
      url: url,
      method: "GET",
    };
  },
  getTaskList(id) {
    return {
      url: `${apiUrl}/tasklists/${id}`,
      method: "GET",
    };
  },
  createTaskList(data) {
    return {
      url: `${apiUrl}/tasklists/`,
      method: "POST",
      data: data,
    };
  },
  deleteTaskList(id) {
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
