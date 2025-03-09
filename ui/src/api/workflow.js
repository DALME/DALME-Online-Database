import { apiUrl } from "./config";

const endpoint = `${apiUrl}/workflow`;

const workflow = {
  changeState(recordId, newState) {
    return {
      url: `${endpoint}/${recordId}/change_state/`,
      method: "PATCH",
      data: newState,
    };
  },
};

export default workflow;
