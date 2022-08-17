import { apiUrl } from "./config";

const endpoint = `${apiUrl}/library`;

const library = {
  getLibrary() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
};

export default library;
