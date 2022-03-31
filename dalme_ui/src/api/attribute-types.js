import { apiUrl } from "./config";

const endpoint = `${apiUrl}/v2/attribute_types`;

const attributeTypes = {
  getAttributeTypes() {
    return new Request(endpoint);
  },
  getAttributeTypesByShortName(shortNames) {
    const url = `${endpoint}/?short_names=${shortNames}`;
    return new Request(url);
  },
};

export default attributeTypes;
