import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attachments`;

const attachments = {
  getAttachment(uuid) {
    const url = `${endpoint}/${uuid}`;
    return new Request(url);
  },
};

export default attachments;
