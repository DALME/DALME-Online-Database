import { apiUrl } from "./config";

const endpoint = `${apiUrl}/users`;

const users = {
  getUsers(query = false) {
    const url = query
      ? `${endpoint}/?${query}`
      : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
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
