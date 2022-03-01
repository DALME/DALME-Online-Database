import S from "string";

import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/tasks`;
const v2Endpoint = `${apiUrl}/v2/tasks`;

const tasks = {
  getTasks() {
    return new Request(endpoint);
  },
  getTask(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getUserTasks(userId) {
    const url = `${v2Endpoint}/?assigned_to=${userId}`;
    return new Request(url);
  },
  createTask(data) {
    const url = `${endpoint}/`;
    return new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });
  },
  editTask(id, data) {
    const url = `${endpoint}/${id}`;
    return new Request(url, {
      method: "PUT",
      headers: headers,
      body: JSON.stringify(data),
    });
  },
  setTaskState(id, action) {
    const url = `${endpoint}/${id}/set_state/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify({ action: S(action).underscore().s }),
    });
  },
  getTaskLists() {
    const url = `${apiUrl}/tasklists`;
    return new Request(url);
  },
  getTaskList(id) {
    const url = `${apiUrl}/tasklists/${id}`;
    return new Request(url);
  },
  createTaskList(data) {
    const url = `${apiUrl}/tasklists/`;
    return new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });
  },
  deleteTaskList(id) {
    const url = `${apiUrl}/tasklists/${id}`;
    return new Request(url, {
      method: "DELETE",
      headers: headers,
    });
  },
  editTaskList(id, data) {
    const url = `${apiUrl}/tasklists/${id}/`;
    return new Request(url, {
      method: "PUT",
      headers: headers,
      body: JSON.stringify(data),
    });
  },
};

export default tasks;
