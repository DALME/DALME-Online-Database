import { apiUrl } from "./config";

const endpoint = `${apiUrl}/pages`;

const pages = {
  list() {
    return {
      url: endpoint,
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

export default pages;
