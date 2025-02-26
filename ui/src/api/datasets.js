import { apiUrl } from "./config";

const endpoint = `${apiUrl}/datasets`;

const datasets = {
  get(data) {
    return {
      url: `${endpoint}/get/`,
      method: "POST",
      data: data,
    };
  },
};

export default datasets;
