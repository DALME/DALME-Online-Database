import { apiUrl } from "./config";
import { defaultOrder } from "./constants";

const endpoint = `${apiUrl}/sources`;

const sources = {
  getSource(objId) {
    const url = `${endpoint}/${objId}`;
    return new Request(url);
  },
  getSources(sourceType, start = 0, length = 25, order = defaultOrder) {
    const data = JSON.stringify({
      draw: 1,
      orderable: true,
      order,
      start,
      length,
    });
    const url = sourceType
      ? `${endpoint}/?class=${sourceType}&data=${data}`
      : `${endpoint}/?data=${data}`;
    return new Request(url);
  },
};

export default sources;
