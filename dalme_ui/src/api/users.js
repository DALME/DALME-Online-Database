import { apiUrl } from "./config";

const endpoint = `${apiUrl}/users`;

const users = {
  getUsers() {
    return {
      url: endpoint,
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
