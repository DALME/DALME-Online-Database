import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tei-elements`;

const teiElements = {
  getElementSets() {
    return {
      url: `${endpoint}/`,
      method: "GET",
    };
  },
};

export default teiElements;
