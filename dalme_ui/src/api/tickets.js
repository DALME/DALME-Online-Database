import { apiUrl, fetchApi } from "./config";

const sources = {
  async userTickets(userId) {
    const params = JSON.stringify({
      draw: 1,
      order: [{ column: 0, dir: "asc" }],
      start: 0,
    });
    const query = `&filter=creation_user,${userId}&data=${params}`;
    const url = `${apiUrl}/tickets/?format=json${query}`;
    const request = new Request(url);

    const response = await fetchApi(request);
    const data = await response.json();

    return { success: response.ok, data };
  },
};

export default sources;
