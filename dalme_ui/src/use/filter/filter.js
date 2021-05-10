import { isEmpty } from "ramda";

const useFilter = (reducer, data) =>
  isEmpty(data) ? data : data.filter((item) => reducer(item));

export default useFilter;
