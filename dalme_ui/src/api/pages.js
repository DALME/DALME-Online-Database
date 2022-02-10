import { apiUrl } from "./config";

const endpoint = `${apiUrl}/pages`;

const pages = {
  getPages() {
    return new Request(endpoint);
  },
};

export default pages;
