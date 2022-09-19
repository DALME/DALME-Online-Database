import { apiUrl } from "./config";
import { defaultOrder } from "./constants";

const endpoint = `${apiUrl}/places`;
const v2Endpoint = `${apiUrl}/v2/places`;

const places = {
  getPlaces(start = 0, length = 25, order = defaultOrder) {
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
  inlineUpdate(data) {
    return {
      url: `${v2Endpoint}/inline_update/`,
      method: "PATCH",
      data: data.value,
    };
  },
};

export default places;
