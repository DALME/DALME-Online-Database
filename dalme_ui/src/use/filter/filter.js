import { isEmpty, isNil } from "ramda";

const useFilter = (reducer, data) =>
  isNil(data) || isEmpty(data) ? [] : data.filter((item) => reducer(item));

export default useFilter;
