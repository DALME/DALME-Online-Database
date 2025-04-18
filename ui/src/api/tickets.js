import S from "string";

import { apiUrl } from "./config";

const endpoint = `${apiUrl}/tickets`;

const tickets = {
  getTickets(query = false) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/?limit=0&offset=0`;
    return {
      url: url,
      method: "GET",
    };
  },
  getTicket(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getUserTickets(userId) {
    return {
      url: `${endpoint}/?creation_user=${userId}`,
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
