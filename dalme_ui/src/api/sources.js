import { apiUrl } from "./config";

const sources = {
  archives() {
    const query = "format=json&class=archives";
    const url = `${apiUrl}/sources/?${query}`;
    return new Request(url);
  },
};

export default sources;
