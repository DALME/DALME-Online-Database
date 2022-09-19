import { apiUrl } from "./config";
import { defaultOrder } from "./constants";

const endpoint = `${apiUrl}/users`;

const users = {
  getUsers(start = 0, length = 25, order = defaultOrder) {
    const data = {
      draw: 1,
      orderable: true,
      order,
      start,
      length,
    };
    return {
      url: `${endpoint}/?data=${JSON.stringify(data)}`,
      method: "GET",
    };
  },
  getUser(username) {
    return {
      url: `${endpoint}/?username=${username}`,
      method: "GET",
    };
  },
  getUserPreferences(userId) {
    return {
      url: `${endpoint}/${userId}/get_preferences/`,
      method: "GET",
    };
  },
  updateUserPreferences(userId, section, key, value) {
    return {
      url: `${endpoint}/${userId}/update_preferences/`,
      method: "POST",
      data: { section, key, value },
    };
  },
};

export default users;
