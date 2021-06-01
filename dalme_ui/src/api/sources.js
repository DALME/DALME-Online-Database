import { apiUrl } from "./config";

const sources = {
  archives() {
    const url = `${apiUrl}/sources/?format=json&class=archives`;
    return new Request(url);
  },
};

export default sources;
