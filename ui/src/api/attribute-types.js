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
  getAttributeTypeOptions(target, serialize = false, model = null, filters = null) {
    let url = `${endpoint}/${target}/opts/`;
    if (model || filters || serialize) {
      const params = [];
      if (model) params.push(`model=${model}`);
      if (filters) params.push(`filters=${filters}`);
      if (serialize) params.push("serialize=true");
      url += `?${params.join("&")}`;
    }

    return {
      url: url,
      method: "GET",
    };
  },
  getAttributeListOptions(list, serialize = false) {
    let url = `${endpoint}/options/?names=${list}`;
    if (serialize) url += "&serialize=True";
    return {
      url: url,
      method: "GET",
    };
  },
};

export default attributeTypes;
