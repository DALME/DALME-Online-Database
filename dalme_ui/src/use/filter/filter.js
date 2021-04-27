const useFilter = (data, reducer) =>
  data && data.length ? data.filter((item) => reducer(item)) : data;

export default useFilter;
