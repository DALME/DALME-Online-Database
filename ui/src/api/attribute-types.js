import { apiUrl } from "./config";

const endpoint = `${apiUrl}/attribute_types`;

const attributeTypes = {
  get() {
    return {
      url: endpoint,
      method: "GET",
    };
  },
  getByShortName(shortNames) {
    return {
      url: `${endpoint}/?short_names=${shortNames}`,
      method: "GET",
    };
  },
  getListOptions(list, serialize = false) {
    let url = `${endpoint}/options_for_list/?names=${list}`;
    if (serialize) url += "&serialize=True";
    return {
      url: url,
      method: "GET",
    };
  },
};

export default attributeTypes;
