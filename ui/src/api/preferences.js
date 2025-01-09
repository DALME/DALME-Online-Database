import { apiUrl } from "./config";

const endpoint = `${apiUrl}/preferences`;

const preferences = {
  getPreferences() {
    return {
      url: `${endpoint}/`,
      method: "GET",
    };
  },
  updatePreferences(key, value) {
    return {
      url: `${endpoint}/${key}/`,
      method: "PUT",
      data: { value: value },
    };
  },
};

export default preferences;
