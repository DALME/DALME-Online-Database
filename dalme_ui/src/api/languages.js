import { apiUrl } from "./config";

const endpoint = `${apiUrl}/languages`;

const languages = {
  getLanguages(orderBy = "name") {
    const url = `${endpoint}/?order_by=${orderBy}`;
    return new Request(url);
  },
};

export default languages;
