import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/sources`;
const v2Endpoint = `${apiUrl}/v2/sources`;

const sourceTypeMap = {
  archive: "archives",
  archivalFile: "archival_files",
  bibliography: "bibliography",
  record: "records",
};

const sources = {
  getSource(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getSources(sourceType, query) {
    // TODO: Remove sourceTypeAPI from routes and use the above map.
    const url = sourceType
      ? `${endpoint}/?class=${sourceType}&${query}`
      : `${endpoint}/?${query}`;
    return new Request(url);
  },
  getSourceOptionsByType(sourceType) {
    const url = `${v2Endpoint}/?class=${sourceTypeMap[sourceType]}&as=options`;
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
    const url = `${endpoint}/${id}/`;
    return new Request(url, {
      method: "PUT",
      headers: headers(),
      body: JSON.stringify(data),
    });
  },
  getBibliographyTypes() {
    const url = `${apiUrl}/content-types/?format=select&id__lt=11`;
    return new Request(url);
  },
};

export default sources;
