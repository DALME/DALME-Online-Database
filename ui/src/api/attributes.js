import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attributes`;

const attributes = {
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  create(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  update(id, payload, patch = true) {
    return {
      url: `${endpoint}/${id}/`,
      method: patch ? "PATCH" : "PUT",
      data: payload,
    };
  },
  destroy(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "DELETE",
    };
  },
  getOptions(target, model = null, filters = null, serialize = false) {
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

  updateValue(target, value) {
    return {
      url: `${endpoint}/${target}/`,
      method: "PATCH",
      data: { value },
    };
  },
};

export default attributes;
