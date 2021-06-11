import S from "string";

import { apiUrl, headers } from "./config";

const tasks = {
  allTasks() {
    const url = `${apiUrl}/tasks`;
    return new Request(url);
  },
  getTask(objId) {
    const url = `${apiUrl}/tasks/${objId}`;
    return new Request(url);
  },
  setTaskState(objId, action) {
    const url = `${apiUrl}/tasks/${objId}/set_state/`;
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
    const query = `filter=assigned_to=${userId}`;
    const url = `${apiUrl}/tasks/?${query}`;
    return new Request(url);
  },
};

export default tasks;
