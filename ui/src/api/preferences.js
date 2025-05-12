import { apiUrl } from "./config";

const endpoint = `${apiUrl}/preferences`;

const preferences = {
  list() {
    return {
      url: `${endpoint}/`,
      method: "GET",
    };
  },
  update(key, value) {
    return {
      url: `${endpoint}/${key}/`,
      method: "PUT",
      data: { value: value },
    };
  },
};

export default preferences;
