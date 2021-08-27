import { apiUrl } from "./config";

const endpoint = `${apiUrl}/agents`;

const agents = {
  getAgents(start = 0, length = 25, order = { column: 0, dir: "asc" }) {
    const data = JSON.stringify({
      draw: 1,
      orderable: true,
      order,
      start,
      length,
    });
    const url = `${endpoint}/?data=${data}`;
    return new Request(url);
  },
};

export default agents;