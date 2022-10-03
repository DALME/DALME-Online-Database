import { apiUrl } from "./config";

const endpoint = `${apiUrl}/countries`;

const countries = {
  getCountries(query = false) {
    const url = query
      ? `${endpoint}/?${query}`
      : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
};

export default countries;
