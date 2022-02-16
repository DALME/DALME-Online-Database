import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sources`;
const v2Endpoint = `${apiUrl}/v2/sources`;

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
  getSourceOptionsByType(sourceType) {
    const url = `${v2Endpoint}/?class=${sourceType}&as=options`;
    return new Request(url);
  },
};

export default sources;
