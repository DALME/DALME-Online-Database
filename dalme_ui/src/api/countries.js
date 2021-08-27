import { apiUrl } from "./config";

const endpoint = `${apiUrl}/countries`;

const countries = {
  getCountries() {
    return new Request(endpoint);
  },
};

export default countries;
