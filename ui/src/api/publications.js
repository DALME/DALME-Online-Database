import { apiUrl } from "./config";

const endpoint = `${apiUrl}/records`;

const publications = {
  getPublication(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getPublications(query) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/`;
    return {
      url: url,
      method: "GET",
    };
  },
};

export default publications;
