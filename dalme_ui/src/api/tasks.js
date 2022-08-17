import S from "string";
import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tasks`;
const v2Endpoint = `${apiUrl}/v2/tasks`;

const tasks = {
  getTasks() {
    return {
      url: endpoint,
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
      url: `${v2Endpoint}/?assigned_to=${userId}`,
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
      url: `${apiUrl}/tasklists`,
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
