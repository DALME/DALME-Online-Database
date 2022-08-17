import { apiUrl } from "./config";

const v2Endpoint = `${apiUrl}/v2/images`;

const images = {
  getImageUrl(damId) {
    return {
      url: `${v2Endpoint}/${damId}/?as=url`,
      method: "GET",
    };
  },
  getImageOptions() {
    return {
      url: `${v2Endpoint}/?as=options`,
      method: "GET",
    };
  },
};

export default images;
