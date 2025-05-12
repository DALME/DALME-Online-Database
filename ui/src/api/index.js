import { apiUrl, coreUrl, publicUrl, purlUrl } from "./config";

const requestOptions = (field, serialize = false, model = null, filters = null) => {
  let url = `${apiUrl}/attribute_types/${field}/opts/`;
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
};

export { publicUrl, apiUrl, coreUrl, purlUrl, requestOptions };

export { fetcher } from "../boot/axios";
export { default as API } from "./api";
export { default as requests } from "./requests";
