import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attributes`;

const attributes = {
  getAttributeOptions(id) {
    return {
      url: `${endpoint}/${id}/options/`,
      method: "GET",
    };
  },
};

export default attributes;
