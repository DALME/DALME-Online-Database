import { apiUrl, headers } from "./config";

const comments = {
  addComment(data) {
    const url = `${apiUrl}/comments/`;
    return new Request(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });
  },
  getComments(model, objId) {
    const url = `${apiUrl}/comments/?model=${model}&object=${objId}`;
    return new Request(url);
  },
};

export default comments;
