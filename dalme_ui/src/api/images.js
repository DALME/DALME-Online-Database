import { apiUrl } from "./config";

const v2Endpoint = `${apiUrl}/v2/images`;

const images = {
  getImageOptions() {
    const url = `${v2Endpoint}/?as=options`;
    return new Request(url);
  },
};

export default images;
