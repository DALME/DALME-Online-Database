import { apiUrl } from "./config";

const endpoint = `${apiUrl}/places`;

const places = {
  getPlaces(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  inlineUpdate(data) {
    return {
      url: `${endpoint}/inline_update/`,
      method: "PATCH",
      data: data.value,
    };
  },
};

export default places;
