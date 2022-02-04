import { apiUrl } from "./config";

const _ = `${apiUrl}/attributes`;
const typesEndpoint = `${apiUrl}/v2/attribute_types`;

const attributes = {
  getAttributeTypes() {
    return new Request(typesEndpoint);
  },
  getAttributeTypesByShortName(short_names) {
    const url = `${typesEndpoint}/?short_names=${short_names}`;
    return new Request(url);
  },
};

export default attributes;
