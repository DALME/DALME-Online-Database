import { slice } from "ramda";

const usePagination = (pageNumber, perPage, data) => {
  const end = pageNumber * perPage;
  const start = end - perPage;
  const pagedData = slice(start, end, data.value);

  return pagedData;
};

export default usePagination;
