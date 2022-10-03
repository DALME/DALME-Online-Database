import { apiUrl } from "./config";

const endpoint = `${apiUrl}/agents`;

const agents = {
  getAgents(query = false) {
    const url = query
      ? `${endpoint}/?${query}`
      : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  getCreditAgents() {
    return {
      url: `${endpoint}/?as=credits`,
      method: "GET",
    };
  },
  getNamedAgents() {
    return {
      url: `${endpoint}/?as=names`,
      method: "GET",
    };
  },
};

export default agents;
