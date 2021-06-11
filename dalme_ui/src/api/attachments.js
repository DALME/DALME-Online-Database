import { apiUrl } from "./config";

const attachments = {
  getAttachment(uuid) {
    const url = `${apiUrl}/attachments/${uuid}`;
    return new Request(url);
  },
};

export default attachments;
