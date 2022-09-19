import { apiUrl } from "./config";
import { defaultOrder } from "./constants";

const endpoint = `${apiUrl}/agents`;
const v2Endpoint = `${apiUrl}/v2/agents`;

const agents = {
  getAgents(start = 0, length = 25, order = defaultOrder) {
    const data = {
      draw: 1,
      orderable: true,
      order,
      start,
      length,
    };
    return {
      url: `${endpoint}/?data=${JSON.stringify(data)}`,
      method: "GET",
    };
  },
  getCreditAgents() {
    return {
      url: `${v2Endpoint}/?as=credits`,
      method: "GET",
    };
  },
  getNamedAgents() {
    return {
      url: `${v2Endpoint}/?as=names`,
      method: "GET",
    };
  },
};

export default agents;
