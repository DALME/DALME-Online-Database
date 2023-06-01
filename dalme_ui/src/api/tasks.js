import S from "string";
import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tasks`;

const tasks = {
  getTasks(query = false) {
    const url = query
      ? `${endpoint}/?${query}`
      : `${endpoint}/?limit=0&offset=0`;
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
  getUserTasks(userId) {
    return {
      url: `${endpoint}/?assigned_to=${userId}`,
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
  getTaskLists() {
    return {
      url: `${apiUrl}/tasklists/`,
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
  editTaskList(id, data) {
    return {
      url: `${apiUrl}/tasklists/${id}/`,
      method: "PUT",
      data: data,
    };
  },
};

export default tasks;
