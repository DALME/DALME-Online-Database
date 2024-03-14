import { apiUrl } from "./config";

const endpoint = `${apiUrl}/images`;

const images = {
  getImageUrl(damId) {
    return {
      url: `${endpoint}/${damId}/?as=url`,
      method: "GET",
    };
  },
  getImageOptions() {
    return {
      url: `${endpoint}/?as=options`,
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
