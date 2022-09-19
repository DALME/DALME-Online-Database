import { apiUrl } from "./config";
import { defaultOrder } from "./constants";

const endpoint = `${apiUrl}/countries`;

const countries = {
  getCountries(start = 0, length = 25, order = defaultOrder) {
    const data = {
      draw: 1,
      orderable: true,
      order,
      start,
      length,
    };
    return {
      url: `${endpoint}/?data=${JSON.stringify(data)}`,
      method: "GET",
    };
  },
};

export default countries;
