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
  getComments(model, id) {
    const url = `${endpoint}/?model=${model}&object=${id}`;
    return new Request(url);
  },
};

export default comments;
