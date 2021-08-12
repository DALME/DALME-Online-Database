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
    const query = `filter=creation_user=${userId}`;
    const url = `${endpoint}/?${query}`;
    return new Request(url);
  },
};

export default tickets;
