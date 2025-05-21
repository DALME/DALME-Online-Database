import { apiUrl } from "./config";

const endpoint = `${apiUrl}/users`;

const users = {
  list(paras = { limit: 0, offset: 0 }) {
    return {
      url: `${endpoint}/?${new URLSearchParams(paras).toString()}`,
      method: "GET",
    };
  },
  get(userId_or_username) {
    return {
      url: `${endpoint}/${userId_or_username}/`,
      method: "GET",
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
};

export default users;
