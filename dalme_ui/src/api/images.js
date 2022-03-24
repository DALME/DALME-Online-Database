import { apiUrl } from "./config";

const v2Endpoint = `${apiUrl}/v2/images`;

const images = {
  getImageUrl(damId) {
    const url = `${v2Endpoint}/${damId}/?as=url`;
    return new Request(url);
  },
  getImageOptions() {
    const url = `${v2Endpoint}/?as=options`;
    return new Request(url);
  },
};

export default images;
