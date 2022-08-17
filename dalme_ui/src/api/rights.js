import { apiUrl } from "./config";

const endpoint = `${apiUrl}/rights`;

const rights = {
  getRights() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
};

export default rights;
