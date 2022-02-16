import { snakeCase } from "change-case";

import { apiUrl } from "./config";

const endpoint = `${apiUrl}/v2/attributes`;

const attributes = {
  getAttributeOptions(shortName) {
    const url = `${endpoint}/?options=${snakeCase(shortName)}`;
    return new Request(url);
  },
};

export default attributes;
