import { apiUrl } from "./config";

const endpoint = `${apiUrl}/comments`;

const comments = {
  add(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  list(model, id) {
    return {
      url: `${endpoint}/?model=${model}&object=${id}&limit=0&offset=0`,
      method: "GET",
    };
  },
};

export default comments;
