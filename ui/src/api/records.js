import { apiUrl } from "./config";

const endpoint = `${apiUrl}/records`;

const records = {
  getRecord(id) {
    return {
      url: `${endpoint}/${id}/`,
      method: "GET",
    };
  },
  getRecords(query) {
    const url = query ? `${endpoint}/?${query}` : `${endpoint}/`;
    return {
      url: url,
      method: "GET",
    };
  },
  createRecord(data) {
    return {
      url: `${endpoint}/`,
      method: "POST",
      data: data,
    };
  },
  editRecord(id, payload, patch = false) {
    return {
      url: `${endpoint}/${id}/`,
      method: patch ? "PATCH" : "PUT",
      data: payload,
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
