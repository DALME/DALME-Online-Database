import { apiUrl } from "./config";

const endpoint = `${apiUrl}/images`;

const images = {
  getUrl(damId) {
    return {
      url: `${endpoint}/${damId}/?as=url`,
      method: "GET",
    };
  },
  getOptions() {
    return {
      url: `${endpoint}/?as=options`,
      method: "GET",
    };
  },
  getInfo(iiif_id) {
    return {
      url: `${iiif_id}/info.json`,
      method: "GET",
    };
  },
};

export default images;
