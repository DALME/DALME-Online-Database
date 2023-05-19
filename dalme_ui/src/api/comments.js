import { apiUrl } from "./config";

const endpoint = `${apiUrl}/comments`;

const comments = {
  addComment(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  getComments(model, id) {
    return {
      url: `${endpoint}/?model=${model}&object=${id}&limit=0&offset=0`,
      method: "GET",
    };
  },
};

export default comments;
