import { apiUrl } from "./config";

const endpoint = `${apiUrl}/v2/attribute_types`;

const attributeTypes = {
  getAttributeTypes() {
    return new Request(endpoint);
  },
  getAttributeTypesByShortName(short_names) {
    const url = `${endpoint}/?short_names=${short_names}`;
    return new Request(url);
  },
};

export default attributeTypes;
