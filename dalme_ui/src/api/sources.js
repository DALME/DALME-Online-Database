import { apiUrl, headers } from "./config";

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
  createSource(data) {
    const url = `${endpoint}/`;
    return new Request(url, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify(data),
    });
  },
  editSource(id, data) {
    const url = `${endpoint}/${id}`;
    return new Request(url, {
      method: "PUT",
      headers: headers(),
      body: JSON.stringify(data),
    });
  },
};

export default sources;
