import { apiUrl } from "./config";

const endpoint = `${apiUrl}/transcriptions`;

const transcriptions = {
  getTranscription(id) {
    return {
      url: `${endpoint}/${id}/`,
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
