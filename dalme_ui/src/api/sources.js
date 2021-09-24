import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sources`;

const sources = {
  getSource(objId) {
    const url = `${endpoint}/${objId}`;
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
