import { apiUrl } from "./config";

const endpoint = `${apiUrl}/choices`;

const choices = {
  getChoices(field) {
    const url = `${endpoint}/?type=model&field=${field}`;
    return new Request(url);
  },
};

export default choices;
