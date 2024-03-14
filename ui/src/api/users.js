import { apiUrl } from "./config";

const endpoint = `${apiUrl}/users`;

const users = {
  getUsers(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  getUser(userId_or_username) {
    return {
      url: `${endpoint}/${userId_or_username}/`,
      method: "GET",
    };
  },
  getUserPreferences(userId_or_username) {
    return {
      url: `${endpoint}/${userId_or_username}/get_preferences/`,
      method: "GET",
    };
  },
  updateUserPreferences(userId_or_username, section, key, value) {
    return {
      url: `${endpoint}/${userId_or_username}/update_preferences/`,
      method: "POST",
      data: { section, key, value },
    };
  },
};

export default users;
