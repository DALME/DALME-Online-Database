import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sources`;

const sourceTypeMap = {
  archive: "archives",
  archivalFile: "archival_files",
  bibliography: "bibliography",
  record: "records",
};

const sources = {
  getSource(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getSources(sourceType, query) {
    // TODO: Remove sourceTypeAPI from routes and use the above map.
    const url = sourceType
      ? `${endpoint}/?class=${sourceType}&${query}`
      : `${endpoint}/?${query}`;
    return {
      url: url,
      method: "GET",
    };
  },
  getSourceOptionsByType(sourceType) {
    return {
      url: `${endpoint}/?class=${sourceTypeMap[sourceType]}&as=options`,
      method: "GET",
    };
  },
  createSource(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  editSource(id, data) {
    return {
      url: `${endpoint}/${id}/`,
      method: "PUT",
      data: data,
    };
  },
  getBibliographyTypes() {
    return {
      url: `${apiUrl}/content-types/?format=select&id__lt=11`,
      method: "GET",
    };
  },
  getSourceManifest(id) {
    return {
      url: `${endpoint}/${id}/get_manifest/`,
      method: "GET",
    };
  },
};

export default sources;
