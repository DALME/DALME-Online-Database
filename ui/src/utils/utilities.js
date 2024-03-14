import { isEmpty, isNil } from "ramda";

export const notNully = (value) => !isNil(value) && !isEmpty(value);

export const formatUuid = (value) =>
  `${value.substr(0, 8)}-${value.substr(8, 4)}-${value.substr(12, 4)}-${value.substr(16, 4)}-${value.substr(20)}`; // eslint-disable-line
