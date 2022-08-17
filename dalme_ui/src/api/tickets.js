import S from "string";
import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tickets`;
const v2Endpoint = `${apiUrl}/v2/tickets`;

const tickets = {
  getTickets() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
  getTicket(id) {
    return {
      url: `${endpoint}/${id}`,
      method: "GET",
    };
  },
  getUserTickets(userId) {
    return {
      url: `${v2Endpoint}/?creation_user=${userId}`,
      method: "GET",
    };
  },
  setTicketState(id, action) {
    return {
      url: `${endpoint}/${id}/set_state/`,
      method: "PATCH",
      data: { action: S(action).underscore().s },
    };
  },
};

export default tickets;
