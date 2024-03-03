import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attribute_types`;

const attributeTypes = {
  getAttributeTypes() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
  getAttributeTypesByShortName(shortNames) {
    return {
      url: `${endpoint}/?short_names=${shortNames}`,
      method: "GET",
    };
  },
};

export default attributeTypes;
