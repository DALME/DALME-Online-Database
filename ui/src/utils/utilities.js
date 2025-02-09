import { isEmpty, isNil } from "ramda";

export const nully = (value) => isNil(value) || isEmpty(value);

export const formatUuid = (value) =>
  `${value.substr(0, 8)}-${value.substr(8, 4)}-${value.substr(12, 4)}-${value.substr(16, 4)}-${value.substr(20)}`; // eslint-disable-line

export const isObject = (obj) => {
  const type = typeof obj;
  return type === "function" || (type === "object" && !!obj);
};

export const isNumber = (val) => !isNaN(parseFloat(val)) && isFinite(val);

export const isInList = (list, value) => {
  const tokens = list.split(",");
  return tokens.includes(value);
};

export const addToList = (list, value) => {
  const tokens = list.split(",");
  tokens.push(value);
  return tokens.join(",");
};

export const removeFromList = (list, value) => {
  let tokens = list.split(",");
  tokens = tokens.filter((x) => x !== value);
  return tokens.join(",");
};
