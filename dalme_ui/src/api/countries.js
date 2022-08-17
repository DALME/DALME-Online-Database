import { apiUrl } from "./config";

const endpoint = `${apiUrl}/countries`;

const countries = {
  getCountries() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
};

export default countries;
