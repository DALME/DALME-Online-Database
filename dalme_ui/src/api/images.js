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
  getImageInfo(iiif_id) {
    return {
      url: `${iiif_id}/info.json`,
      method: "GET",
    };
  },
};

export default images;
