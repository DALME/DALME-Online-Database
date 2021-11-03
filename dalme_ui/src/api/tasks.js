import S from "string";

import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/tasks`;

const tasks = {
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
  userTasks(userId) {
    // TODO: This does nothing right now, add new endpoint.
    const query = `stubbed=${userId}`;
    const url = `${endpoint}/?${query}`;
    return new Request(url);
  },
};

export default tasks;
