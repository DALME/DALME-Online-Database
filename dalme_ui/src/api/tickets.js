import { apiUrl } from "./config";

const tickets = {
  allTickets() {
    const url = `${apiUrl}/tickets`;
    return new Request(url);
  },
  getTicket(objId) {
    const url = `${apiUrl}/tickets/${objId}`;
    return new Request(url);
  },
  userTickets(userId) {
    const query = `filter=creation_user=${userId}`;
    const url = `${apiUrl}/tickets/?${query}`;
    return new Request(url);
  },
};

export default tickets;
