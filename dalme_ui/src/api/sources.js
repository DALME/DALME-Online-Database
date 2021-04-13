import { apiUrl, fetchApi } from "./config";

const sources = {
  async archives() {
    const url = `${apiUrl}/sources/?format=json&class=archives`;
    const request = new Request(url);

    const response = await fetchApi(request);
    const data = await response.json();

    return { success: response.ok, data };
  },
};

export default sources;
