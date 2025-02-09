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
  getAttributeOptions(target, serialize = false) {
    let url = `${endpoint}/${target}/options/`;
    if (serialize) url += "?serialize=True";
    return {
      url: url,
      method: "GET",
    };
  },
};

export default attributeTypes;
