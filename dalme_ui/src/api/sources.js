import { apiUrl } from "./config";

const endpoint = `${apiUrl}/sources`;

const sources = {
  getSource(objId) {
    const url = `${endpoint}/${objId}`;
    return new Request(url);
  },
  getSources(kind, start = 0, length = 25, order = { column: 0, dir: "asc" }) {
    // TODO: Move order to constant somewhere.
    // const serverSideSchema = yup.object.shape({});
    const data = JSON.stringify({
      draw: 1,
      orderable: true,
      order,
      start,
      length,
    });
    const url = kind
      ? `${endpoint}/?class=${kind}&data=${data}`
      : `${endpoint}/?data=${data}`;
    return new Request(url);
  },
};

export default sources;
