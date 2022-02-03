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
  setTicketState(id, action) {
    const url = `${endpoint}/${id}/set_state/`;
    return new Request(url, {
      method: "PATCH",
      headers: headers,
      body: JSON.stringify({ action: S(action).underscore().s }),
    });
  },
  userTickets(userId) {
    // TODO: This does nothing right now, add new endpoint.
    const query = `stubbed=${userId}`;
    const url = `${endpoint}/?${query}`;
    return new Request(url);
  },
};

export default tickets;
