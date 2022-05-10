import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/places`;

const places = {
  getPlaces() {
    return new Request(endpoint);
  },
  updatePlaces(data) {
    const url = `${endpoint}/update_places/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers(),
      body: JSON.stringify(data.value),
    });
  },
};

export default places;
