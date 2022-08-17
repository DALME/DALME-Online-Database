import { apiUrl } from "./config";

const endpoint = `${apiUrl}/languages`;

const languages = {
  getLanguages(orderBy = "name") {
    return {
      url: `${endpoint}/?order_by=${orderBy}`,
      method: "GET",
    };
  },
};

export default languages;
