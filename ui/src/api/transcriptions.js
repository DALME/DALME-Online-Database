import { apiUrl } from "./config";

const endpoint = `${apiUrl}/transcriptions`;

const transcriptions = {
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
  checkVersion(id, version) {
    return {
      url: `${endpoint}/${id}/check_version/?v=${version}`,
      method: "GET",
    };
  },
};

export default transcriptions;
