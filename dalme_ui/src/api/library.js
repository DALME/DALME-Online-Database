import { apiUrl } from "./config";

const endpoint = `${apiUrl}/library`;

const library = {
  getLibrary() {
    return new Request(endpoint);
  },
};

export default library;
