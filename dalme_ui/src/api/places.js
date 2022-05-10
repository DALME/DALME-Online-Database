import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/places`;
const v2Endpoint = `${apiUrl}/v2/places`;

const places = {
  getPlaces() {
    return new Request(endpoint);
  },
  inlineUpdate(data) {
    const url = `${v2Endpoint}/inline_update/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers(),
      body: JSON.stringify(data.value),
    });
  },
};

export default places;
