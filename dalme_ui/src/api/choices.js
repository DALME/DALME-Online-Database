import { apiUrl } from "./config";

const endpoint = `${apiUrl}/choices`;

const choices = {
  getChoices(field) {
    return {
      url: `${endpoint}/?type=model&field=${field}`,
      method: "GET",
    };
  },
};

export default choices;
