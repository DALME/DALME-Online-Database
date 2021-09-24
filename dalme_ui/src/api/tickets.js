import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tickets`;

const tickets = {
  getTickets() {
    return new Request(endpoint);
  },
  getTicket(objId) {
    const url = `${endpoint}/${objId}`;
    return new Request(url);
  },
  userTickets(userId) {
    // TODO: This does nothing right now, add new endpoint.
    const query = `stubbed=${userId}`;
    const url = `${endpoint}/?${query}`;
    return new Request(url);
  },
};

export default tickets;
