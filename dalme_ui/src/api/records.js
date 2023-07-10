import { apiUrl } from "./config";

const endpoint = `${apiUrl}/records`;

const records = {
  getRecord(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getRecords(query) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/`;
    return {
      url: url,
      method: "GET",
    };
  },
  // getSourceOptionsByType(sourceType) {
  //   return {
  //     url: `${endpoint}/?class=${sourceTypeMap[sourceType]}&as=options`,
  //     method: "GET",
  //   };
  // },
  // createSource(data) {
  //   return {
  //     url: `${endpoint}/`,
  //     method: "POST",
  //     data: data,
  //   };
  // },
  // editSource(id, data) {
  //   return {
  //     url: `${endpoint}/${id}/`,
  //     method: "PUT",
  //     data: data,
  //   };
  // },
  // getSourceManifest(id) {
  //   return {
  //     url: `${endpoint}/${id}/get_manifest/`,
  //     method: "GET",
  //   };
  // },
};

export default records;
