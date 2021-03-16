import { apiUrl, fetchApi } from "./config";

const sources = {
  async archives() {
    const url = `${apiUrl}/sources/?format=json&class=archives`;
    const request = new Request(url);

    const response = await fetchApi(request);
    return response;
  },
};

export default sources;
