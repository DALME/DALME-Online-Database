import { apiUrl } from "./config";

const endpoint = `${apiUrl}/rights`;

const rights = {
  getRights() {
    return new Request(endpoint);
  },
};

export default rights;
