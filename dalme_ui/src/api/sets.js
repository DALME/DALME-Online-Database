import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sets`;

const sets = {
  getSet(objId) {
    const url = `${endpoint}/${objId}`;
    return new Request(url);
  },
  getSets(setType) {
    const url = `${endpoint}/?set_type=${setType}`;
    return new Request(url);
  },
};

export default sets;
