import { apiUrl } from "./config";

const endpoint = `${apiUrl}/users`;

const users = {
  getUsers() {
    return new Request(endpoint);
  },
  getUser(username) {
    const url = `${endpoint}/?username=${username}`;
    return new Request(url);
  },
};

export default users;
