import { slice } from "ramda";

const usePagination = (pageNumber, perPage, data) => {
  const end = pageNumber * perPage;
  const start = end - perPage;
  return slice(start, end, data.value);
};

export default usePagination;
