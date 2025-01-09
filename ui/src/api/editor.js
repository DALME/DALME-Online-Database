import { apiUrl } from "./config";

const endpoint = `${apiUrl}/editor`;

const editor = {
  getTagSets() {
    return {
      url: `${endpoint}/`,
      method: "GET",
    };
  },
};

export default editor;
