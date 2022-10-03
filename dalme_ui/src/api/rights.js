import { apiUrl } from "./config";

const endpoint = `${apiUrl}/rights`;

const rights = {
  getRights(query = false) {
    const url = query
      ? `${endpoint}/?${query}`
      : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
};

export default rights;
