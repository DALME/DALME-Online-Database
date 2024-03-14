import { reduce } from "ramda";

export const merge = (...schemas) => {
  const [first, ...rest] = schemas;
  return reduce((mergedSchemas, schema) => mergedSchemas.concat(schema), first, rest);
};
