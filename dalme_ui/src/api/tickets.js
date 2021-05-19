import { apiUrl } from "./config";

const sources = {
  userTickets(userId) {
    const params = JSON.stringify({
      draw: 1,
      order: [{ column: 0, dir: "asc" }],
      start: 0,
    });
    const query = `&filter=creation_user,${userId}&data=${params}`;
    const url = `${apiUrl}/tickets/?format=json${query}`;
    return new Request(url);
  },
};

export default sources;
