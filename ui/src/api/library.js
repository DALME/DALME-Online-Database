import { apiUrl } from "./config";

const endpoint = `${apiUrl}/library`;

const library = {
  list() {
    return {
      url: `${endpoint}/`,
      method: "GET",
    };
  },
};

export default library;
