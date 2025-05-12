import { apiUrl } from "./config";

const endpoint = `${apiUrl}/records`;

const records = {
  get(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  list(query) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/`;
    return {
      url: url,
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
  metadata() {
    return {
      url: `${endpoint}/metadata/`,
      method: "GET",
    };
  },
  addAttribute(id, type, value) {
    return {
      url: `${endpoint}/${id}/add_attribute/`,
      method: "PATCH",
      data: { type, value },
    };
  },
  updateRelated(id, field, value) {
    return {
      url: `${endpoint}/${id}/update_related/`,
      method: "PATCH",
      data: { field, value },
    };
  },
};

export default records;
