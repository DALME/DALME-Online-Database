import { snakeCase } from "change-case";
import { apiUrl } from "./config";

const endpoint = `${apiUrl}/v2/attributes`;

const attributes = {
  getAttributeOptions(shortName) {
    return {
      url: `${endpoint}/?options=${snakeCase(shortName)}`,
      method: "GET",
    };
  },
};

export default attributes;