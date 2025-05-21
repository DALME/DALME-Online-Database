import { apiUrl } from "./config";

const endpoint = `${apiUrl}/preferences`;

const preferences = {
  list() {
    return {
      url: `${endpoint}/`,
      method: "GET",
    };
  },
  update(key, payload) {
    return {
      url: `${endpoint}/${key}/`,
      method: "PUT",
      data: payload,
    };
  },
};

export default preferences;
