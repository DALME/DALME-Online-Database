import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sources`;

const sources = {
  getSource(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getSources(sourceType, query) {
    const url = sourceType
      ? `${endpoint}/?class=${sourceType}&${query}`
      : `${endpoint}/?${query}`;
    return new Request(url);
  },
};

export default sources;
