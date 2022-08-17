import { apiUrl } from "./config";

const endpoint = `${apiUrl}/pages`;

const pages = {
  getPages() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
};

export default pages;
