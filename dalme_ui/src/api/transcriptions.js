import { apiUrl } from "./config";

const endpoint = `${apiUrl}/transcriptions`;

const transcriptions = {
  getTranscription(id) {
    return {
      url: `${endpoint}/${id}`,
      method: "GET",
    };
  },
};

export default transcriptions;
