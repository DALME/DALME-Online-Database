import S from "string";

import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/tasks`;

const tasks = {
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
  getTasks() {
    return new Request(endpoint);
  },
  getTask(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  setTaskState(id, action) {
    const url = `${endpoint}/${id}/set_state/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify({ action: S(action).underscore().s }),
    });
  },
  taskLists() {
    const url = `${apiUrl}/tasklists`;
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
  getTaskList(id) {
    const url = `${apiUrl}/tasklists/${id}`;
    return new Request(url);
  },
  userTasks(userId) {
    // TODO: This does nothing right now, add new endpoint.
    const query = `stubbed=${userId}`;
    const url = `${endpoint}/?${query}`;
    return new Request(url);
  },
};

export default tasks;
