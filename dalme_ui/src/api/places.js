import { apiUrl } from "./config";

const endpoint = `${apiUrl}/places`;

const places = {
  getPlaces() {
    return new Request(endpoint);
  },
};

export default places;
