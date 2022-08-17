import { apiUrl } from "./config";

const endpoint = `${apiUrl}/places`;
const v2Endpoint = `${apiUrl}/v2/places`;

const places = {
  getPlaces() {
    return {
      url: endpoint,
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
