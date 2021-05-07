const useFilter = (reducer, data) =>
  data && data.length ? data.filter((item) => reducer(item)) : data;

export default useFilter;
