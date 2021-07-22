import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/comments`;

const comments = {
  addComment(data) {
    const url = `${endpoint}/`;
    return new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });
  },
  getComments(model, objId) {
    const url = `${endpoint}/?model=${model}&object=${objId}`;
    return new Request(url);
  },
};

export default comments;
