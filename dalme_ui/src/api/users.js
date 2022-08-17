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
};

export default users;
