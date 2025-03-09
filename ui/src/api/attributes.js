import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attributes`;

const attributes = {
  getAttributeOptions(target, model = null, filters = null, serialize = false) {
    let url = `${endpoint}/${target}/options/`;
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

  updateAttributeValue(target, value) {
    return {
      url: `${endpoint}/${target}/`,
      method: "PATCH",
      data: { value },
    };
  },
};

export default attributes;
