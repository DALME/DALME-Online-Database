import { isEmpty, isNil } from "ramda";

export const notNully = (value) => !isNil(value) && !isEmpty(value);
