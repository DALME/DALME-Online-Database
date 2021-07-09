import { apiUrl } from "./config";

const sources = {
  getSources(kind) {
    const endpoint = `${apiUrl}/sources/`;
    const data = JSON.stringify({
      draw: 1,
      start: 0,
      length: 25,
      orderable: true,
      order: [{ column: 0, dir: "asc" }],
    });
    const url = kind
      ? `${endpoint}?class=${kind}&data=${data}`
      : `${endpoint}?data=${data}`;
    return new Request(url);
  },
};

export default sources;
