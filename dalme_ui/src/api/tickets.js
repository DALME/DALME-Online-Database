import S from "string";

import { apiUrl, headers } from "./config";

const endpoint = `${apiUrl}/tickets`;

const tickets = {
  getTickets() {
    return new Request(endpoint);
  },
  getTicket(id) {
    const url = `${endpoint}/${id}`;
    return new Request(url);
  },
  getUserTickets(userId) {
    const url = `${endpoint}/?assigned_to=${userId}`;
    return new Request(url);
  },
  setTicketState(id, action) {
    const url = `${endpoint}/${id}/set_state/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify({ action: S(action).underscore().s }),
    });
  },
};

export default tickets;
