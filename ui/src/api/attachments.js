import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attachments`;

const attachments = {
  getAttachment(uuid) {
    return {
      url: `${endpoint}/${uuid}/`,
      method: "GET",
    };
  },
};

export default attachments;
